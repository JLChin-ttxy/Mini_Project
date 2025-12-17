// ============================================================================
// UTAR AI Chatbot - Ultimate Backend (Name & ID Support)
// ============================================================================
const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// Database Connection
const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '!Org0131', // CHECK YOUR PASSWORD
    database: process.env.DB_NAME || 'university_admission_db',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// Helper: Format Dialogflow Response
function formatDialogflowResponse(text) {
    return {
        fulfillmentText: text,
        fulfillmentMessages: [{ text: { text: [text] } }]
    };
}

// Helper: Extract Parameters
function extractParameters(req) {
    return req.body.queryResult.parameters || {};
}

// ============================================================================
// SMART HELPER: Resolve Program ID from Name OR Number
// ============================================================================
async function resolveProgram(input) {
    if (!input) return null;
    
    // If input is purely a number (e.g., "25"), assume it's an ID
    if (/^\d+$/.test(input)) {
        const [rows] = await pool.execute(
            `SELECT program_id, program_name, level, duration_years, faculty_id, career_prospects, description FROM PROGRAM WHERE program_id = ?`, 
            [input]
        );
        return rows.length > 0 ? rows[0] : null;
    } 
    
    // If input is text (e.g., "Computer Science"), search by name
    else {
        const [rows] = await pool.execute(
            `SELECT * FROM PROGRAM WHERE program_name LIKE ? LIMIT 1`, 
            [`%${input}%`]
        );
        return rows.length > 0 ? rows[0] : null;
    }
}

// ============================================================================
// WEBHOOK HANDLER
// ============================================================================
app.post('/webhook', async (req, res) => {
    try {
        const intentName = req.body.queryResult.intent.displayName;
        const params = extractParameters(req);
        console.log(`📩 Intent: ${intentName} | Params:`, params);

        let responseText = "I'm not sure how to help with that.";

        switch (intentName) {
            // ================================================================
            // MODULE 1: ACADEMIC PROGRAMS
            // ================================================================
            case 'SearchPrograms': {
                let query = `
                    SELECT p.program_name 
                    FROM PROGRAM p
                    JOIN FACULTY f ON p.faculty_id = f.faculty_id
                    WHERE 1=1
                `;
                let qParams = [];

                if (params.faculty) { 
                    query += ` AND f.faculty_name LIKE ?`; 
                    qParams.push(`%${params.faculty}%`); 
                }
                if (params.programName) { 
                    query += ` AND p.program_name LIKE ?`; 
                    qParams.push(`%${params.programName}%`); 
                }
                if (params.level) { 
                    query += ` AND p.level = ?`; 
                    qParams.push(params.level); 
                }
                
                query += ` ORDER BY p.program_id LIMIT 40`; 
                
                const [programs] = await pool.execute(query, qParams);

                if (programs.length === 0) {
                    responseText = "🚫 No programs found matching your criteria.";
                } else {
                    responseText = "🎓 **Found Programs:**\n\n";
                    
                    // MODIFIED LOOP: Displays strictly the name only
                    programs.forEach((p, index) => {
                        responseText += `${index + 1}. ${p.program_name}\n`;
                    });
                    
                }
                break;
            }

            case 'GetProgramDetails': {
                const prog = await resolveProgram(params.programId);
                
                if (!prog) {
                    responseText = `❌ I couldn't find a program matching "**${params.programId}**".\nPlease check the spelling or try a keyword.`;
                } else {
                    const [fac] = await pool.execute(`SELECT faculty_name FROM FACULTY WHERE faculty_id = ?`, [prog.faculty_id]);
                    
                    // Fetch Subjects
                    const [subs] = await pool.execute(`
                        SELECT s.subject_name, s.credit_hours 
                        FROM PROGRAM_SUBJECT ps 
                        JOIN SUBJECT s ON ps.subject_id = s.subject_id 
                        WHERE ps.program_id = ? LIMIT 5`, [prog.program_id]);
                    
                    let subjectList = subs.length > 0 
                        ? subs.map(s => `   • ${s.subject_name} (${s.credit_hours} Cr)`).join('\n')
                        : "   • No subjects listed yet.";

                    // FORMATTING FIX: Clear sections with headers
                    responseText = `📘 **${prog.program_name}**\n` +
                                   `────────────────────\n` + 
                                   `🏢 **Faculty:** ${fac[0].faculty_name}\n` +
                                   `⏳ **Duration:** ${prog.duration_years} Years\n` +
                                   `🎓 **Level:** ${prog.level}\n\n` +
                                   
                                   `📝 **Description**\n${prog.description}\n\n` +
                                   
                                   `📚 **Key Subjects**\n${subjectList}\n\n` +
                                   
                                   `💼 **Career Prospects**\n${prog.career_prospects}\n\n` + 
                                   
                                   `_Want to apply? Ask "How do I apply for program [id]?"_`;
                }
                break;
            }

            case 'ComparePrograms':
                console.log('🔍 ComparePrograms intent triggered');
                console.log('Parameters:', params);
                
                let programIds = [];
                
                if (params.programIds) {
                    programIds = Array.isArray(params.programIds) 
                        ? params.programIds 
                        : [params.programIds];
                } else if (params.programId1 && params.programId2) {
                    programIds = [params.programId1, params.programId2];
                }
                
                programIds = programIds
                    .map(id => parseInt(id))
                    .filter(id => !isNaN(id) && id > 0);
                
                console.log('Processed programIds:', programIds);
                
                if (programIds.length < 2) {
                    responseText = '⚠️ Please provide 2 program IDs to compare.\n\n' +
                                'Example: "Compare program 1 and 2"';
                } else {
                    try {
                        const id1 = programIds[0];
                        const id2 = programIds[1];
                        
                        // Fetch both programs
                        const [programs] = await pool.execute(
                            `SELECT 
                                p.program_id,
                                p.program_name,
                                p.level,
                                p.duration_years,
                                p.career_prospects,
                                f.faculty_name
                            FROM PROGRAM p
                            JOIN FACULTY f ON p.faculty_id = f.faculty_id
                            WHERE p.program_id IN (?, ?)
                            ORDER BY p.program_id`,
                            [id1, id2]
                        );
                        
                        if (programs.length < 2) {
                            responseText = '⚠️ I couldn\'t find one or both of those programs. Please check the program IDs.\n\n' +
                                        'Try asking: "What programs do you offer?" to see available programs.';
                        } else {
                            const prog1 = programs.find(p => p.program_id === id1);
                            const prog2 = programs.find(p => p.program_id === id2);
                            
                            // Get total fees (sum all semesters) - USING 'amount' COLUMN
                            const [fees1] = await pool.execute(
                                `SELECT SUM(amount) as total, currency FROM TUITION_FEE WHERE program_id = ? GROUP BY currency`,
                                [id1]
                            );
                            
                            const [fees2] = await pool.execute(
                                `SELECT SUM(amount) as total, currency FROM TUITION_FEE WHERE program_id = ? GROUP BY currency`,
                                [id2]
                            );
                            
                            const total1 = fees1[0]?.total 
                                ? `${fees1[0].currency || 'RM'} ${parseFloat(fees1[0].total).toLocaleString('en-MY', {minimumFractionDigits: 2, maximumFractionDigits: 2})}` 
                                : 'N/A';
                                
                            const total2 = fees2[0]?.total 
                                ? `${fees2[0].currency || 'RM'} ${parseFloat(fees2[0].total).toLocaleString('en-MY', {minimumFractionDigits: 2, maximumFractionDigits: 2})}` 
                                : 'N/A';
                            
                            responseText = `⚖️ Program Comparison:\n\n` +
                                        `1️⃣ ${prog1.program_name}\n` +
                                        `   Faculty: ${prog1.faculty_name}\n` +
                                        `   Level: ${prog1.level}\n` +
                                        `   Duration: ${prog1.duration_years} years\n` +
                                        `   Total Fees: ${total1}\n\n` +
                                        `2️⃣ ${prog2.program_name}\n` +
                                        `   Faculty: ${prog2.faculty_name}\n` +
                                        `   Level: ${prog2.level}\n` +
                                        `   Duration: ${prog2.duration_years} years\n` +
                                        `   Total Fees: ${total2}\n\n`;
                        }
                    } catch (error) {
                        console.error('❌ Error in ComparePrograms:', error);
                        responseText = 'I encountered an error while comparing programs. Please try again.';
                    }
                }
                break;
            
            
            

            case 'GetFacultyMembers': {
                const [members] = await pool.execute(
                    `SELECT * FROM FACULTY_MEMBER JOIN FACULTY ON FACULTY_MEMBER.faculty_id = FACULTY.faculty_id WHERE FACULTY.faculty_name LIKE ? LIMIT 4`, 
                    [`%${params.faculty}%`]
                );
                
                if (members.length === 0) {
                    responseText = "🚫 No faculty members found.";
                } else {
                    responseText = `👨‍🏫 **Faculty Members (${params.faculty}):**\n\n`;
                    members.forEach(m => {
                        responseText += `👤 **${m.name}**\n   ${m.designation} - ${m.specialization}\n   📧 ${m.email}\n\n`;
                    });
                }
                break;
            }

            // ================================================================
            // MODULE 2: ADMISSION REQUIREMENTS
            // ================================================================
            case 'GetAdmissionRequirements': {
                const prog = await resolveProgram(params.programId);
                if (!prog) {
                    responseText = `❌ Program "${params.programId}" not found.`;
                } else {
                    const [reqs] = await pool.execute(`SELECT * FROM ADMISSION_REQUIREMENT WHERE program_id = ?`, [prog.program_id]);
                    if (reqs.length === 0) {
                        responseText = "ℹ️ Standard university requirements apply.";
                    } else {
                        responseText = `📋 **Requirements for ${prog.program_name}:**\n\n`;
                        reqs.forEach(r => {
                            responseText += `✅ **${r.qualification_type}**: ${r.minimum_grade}\n   ${r.additional_requirements || ''}\n\n`;
                        });
                    }
                }
                break;
            }

            case 'GetImportantDates':
                console.log('📅 GetImportantDates intent triggered');
                console.log('Parameters:', params);
                
                const importantDatesProgramId = params.programId || params.program_id;
                
                if (!importantDatesProgramId) {
                    responseText = '📅 General Important Dates:\n\n' +
                                '🗓️ Intake Periods:\n' +
                                '   • January Intake\n' +
                                '   • May Intake\n' +
                                '   • October Intake\n\n' +
                                'For specific program dates, ask:\n' +
                                '"What are the important dates for program [ID]?"';
                } else {
                    try {
                        // Fetch program
                        const [programs] = await pool.execute(
                            `SELECT program_name FROM PROGRAM WHERE program_id = ?`,
                            [importantDatesProgramId]
                        );
                        
                        if (programs.length === 0) {
                            responseText = '❌ Program not found. Please check the program ID.';
                        } else {
                            const programName = programs[0].program_name;
                            
                            // Fetch important dates - FIX SQL SYNTAX
                            const [dates] = await pool.execute(
                                `SELECT * FROM IMPORTANT_DATE WHERE program_id = ? ORDER BY start_date`,
                                [importantDatesProgramId]
                            );
                            
                            if (dates.length === 0) {
                                responseText = `📅 Important Dates for ${programName}:\n\n` +
                                            '🗓️ General intake periods:\n' +
                                            '   • January Intake\n' +
                                            '   • May Intake\n' +
                                            '   • October Intake\n\n' +
                                            'Specific dates to be announced.';
                            } else {
                                responseText = `📅 Important Dates for ${programName}:\n\n`;

                                // Group trimester dates
                                const trimesterDates = dates.filter(d => d.event_type.includes('Trimester'));
                                if (trimesterDates.length > 0) {
                                    responseText += `🎓 ACADEMIC CALENDAR:\n`;
                                    trimesterDates.forEach(d => {
                                        const start = d.start_date ? new Date(d.start_date).toLocaleDateString('en-MY') : 'TBA';
                                        const type = d.event_type.includes('Start') ? '▶️' : '⏹️';
                                        responseText += `   ${type}: ${start}\n`;
                                        if (d.description) responseText += `     ${d.description}\n`;
                                    });
                                }
                            }
                        }
                    } catch (error) {
                        console.error('❌ Error in GetImportantDates:', error);
                        responseText = 'I encountered an error fetching important dates. Please try again.';
                    }
                }
                break;

            case 'GetApplicationProcedure': {
                responseText = "🚀 **How to Apply:**\n1️⃣ Browse our programs and verify entry requirements.\n2️⃣ Gather documents.\n3️⃣ Fill out the form at admission page.\n4️⃣ Receive your offer and pay the registration fee.\n";
                break;
            }

            case 'GetDocumentChecklist': {
                const prog = await resolveProgram(params.programId);
                if (!prog) {
                    responseText = "❌ Program not found.";
                } else {
                    const [docs] = await pool.execute(`SELECT * FROM DOCUMENT_CHECKLIST WHERE program_id = ?`, [prog.program_id]);
                    responseText = `🗂️ **Documents for ${prog.program_name}:**\n`;
                    docs.forEach(d => responseText += `${d.is_mandatory ? '❗' : '⚪'} ${d.document_name}\n`);
                }
                break;
            }

            case 'CheckApplicationStatus': {
                const [app] = await pool.execute(`SELECT status, remarks FROM APPLICATION WHERE reference_number = ?`, [params.referenceNumber]);
                if (app.length === 0) {
                    responseText = "⚠️ Application not found. Check your reference number.";
                } else {
                    responseText = `🔎 **Status:** ${app[0].status}\n💬 **Remarks:** ${app[0].remarks || 'None'}`;
                }
                break;
            }

            // ================================================================
            // MODULE 3: TUITION FEES & SCHOLARSHIPS
            // ================================================================
            case 'GetTuitionFees': {
                const prog = await resolveProgram(params.programId);
                if (!prog) {
                    responseText = "❌ Program not found.";
                } else {
                    const [fees] = await pool.execute(`SELECT * FROM TUITION_FEE WHERE program_id = ?`, [prog.program_id]);
                    responseText = `💸 **Fees for ${prog.program_name}:**\n`;
                    fees.forEach(f => responseText += `- Sem ${f.semester}: RM ${f.amount}\n`);
                }
                break;
            }

            case 'CalculateTotalCost': {
                const prog = await resolveProgram(params.programId);
                if (!prog) {
                    responseText = "❌ Program not found.";
                } else {
                    const [total] = await pool.execute(`SELECT SUM(amount) as total FROM TUITION_FEE WHERE program_id = ?`, [prog.program_id]);
                    responseText = `💰 **Total Tuition (${prog.program_name}):**\nRM ${total[0].total || 'Unknown'}\n(Excludes living costs)`;
                }
                break;
            }

            case 'SearchScholarships': {
                const [schol] = await pool.execute(`SELECT * FROM SCHOLARSHIP LIMIT 3`);
                responseText = "🎓 **Available Scholarships:**\n\n";
                schol.forEach(s => {
                    responseText += `🌟 **${s.scholarship_name}**\n   Amt: RM ${s.amount}\n   Deadline: ${s.application_deadline}\n\n`;
                });
                break;
            }

            case 'GetFinancialAid': {
                const [aid] = await pool.execute(`SELECT * FROM FINANCIAL_AID`);
                responseText = "🤝 **Financial Aid Options:**\n\n";
                aid.forEach(a => {
                    responseText += `🔹 **${a.aid_name}** (${a.aid_type})\n   Criteria: ${a.eligibility_criteria}\n\n`;
                });
                break;
            }

            // ================================================================
            // MODULE 4: CAMPUS FACILITIES & LIFE
            // ================================================================
            case 'GetCampusFacilities': {
                const [fac] = await pool.execute(`SELECT facility_name, description FROM CAMPUS_FACILITY LIMIT 4`);
                responseText = "🏢 **Campus Facilities:**\n\n";
                fac.forEach(f => responseText += `🔹 **${f.facility_name}**: ${f.description}\n`);
                break;
            }

            case 'GetAccommodation': {
                const [acc] = await pool.execute(`SELECT * FROM ACCOMMODATION LIMIT 3`);
                responseText = "🏠 **Accommodation Options:**\n\n";
                acc.forEach(a => {
                    responseText += `🛏️ **${a.hostel_name}** (${a.room_type})\n   Fee: RM ${a.monthly_fee}/month\n   Vacancy: ${a.available_slots} slots\n\n`;
                });
                break;
            }

            case 'GetStudentClubs': {
                const [clubs] = await pool.execute(`SELECT club_name, category FROM STUDENT_CLUB LIMIT 5`);
                responseText = "🎭 **Student Clubs:**\n";
                clubs.forEach(c => responseText += `• ${c.club_name} (${c.category})\n`);
                break;
            }

            case 'GetUpcomingEvents': {
                const [events] = await pool.execute(`SELECT event_name, event_date, location FROM EVENT WHERE event_date >= CURDATE() LIMIT 3`);
                if (events.length === 0) responseText = "📅 No upcoming events scheduled.";
                else {
                    responseText = "🎉 **Upcoming Events:**\n\n";
                    events.forEach(e => responseText += `🗓️ **${e.event_name}**\n   Date: ${e.event_date.toString().split('T')[0]}\n   Loc: ${e.location}\n\n`);
                }
                break;
            }

            case 'SearchFAQ': {
                const keyword = params.keyword || '';
                const [faqs] = await pool.execute(`SELECT question, answer FROM FAQ WHERE question LIKE ? OR category LIKE ? LIMIT 20`, [`%${keyword}%`, `%${keyword}%`]);
                
                if (faqs.length === 0) {
                    responseText = "❓ I don't have an answer for that yet. Please contact support.";
                } else {
                    responseText = `**Q:** ${faqs[0].question}\n**A:** ${faqs[0].answer}`;
                }
                break;
            }

            case 'Default Welcome Intent':
                responseText = "👋 Hi! I'm the UTAR AI Assistant.\nAsk me about **Programs**, **Admissions**, **Fees**, **Scholarships**, or **Campus Life**!";
                break;
        }

        res.json(formatDialogflowResponse(responseText));

    } catch (error) {
        console.error("❌ Error:", error);
        res.json(formatDialogflowResponse("⚠️ System error. Please try again later."));
    }
});

app.listen(PORT, () => console.log(`🚀 UTAR Chatbot Server running on port ${PORT}`));