# Dialogflow Setup Guide - Fixing `{@program_name}` Issue

## Problem
Dialogflow is showing `{@program_name}` as literal text instead of calling your webhook. This means Dialogflow is using a **static response template** instead of your webhook.

## Solution: Configure Dialogflow Correctly

### Step 1: Remove Static Response Templates

1. **Open your Dialogflow agent**
2. **Go to the intent** that handles program queries (e.g., "get_program_requirements")
3. **Scroll down to "Responses" section**
4. **DELETE all static response templates** that look like:
   ```
   The requirements for {@program_name} can be view via the link:
   http://172.20.10.3:5000/admission/requirements
   ```
5. **Remove ALL text responses** - you only want the webhook to respond

### Step 2: Enable Webhook Fulfillment

1. **In the same intent**, scroll to **"Fulfillment"** section (at the bottom)
2. **Enable "Enable webhook call for this intent"** ✅
3. **Make sure it's checked/enabled**

### Step 3: Configure Webhook URL

1. **Go to Settings** (gear icon) → **Fulfillment**
2. **Enable "Webhook"**
3. **Add your webhook URL:**
   ```
   http://172.20.10.3:5000/dialogflow-webhook
   ```
4. **Click "Save"**

### Step 4: Configure Entity Extraction

1. **Go to the intent** → **"Training phrases"** section
2. **Add training phrases** like:
   - "Requirements for Foundation in Science"
   - "Requirements for Foundation in Arts"
   - "What are the requirements for Foundation in Science"
   - "I need requirements for Foundation in Arts"
3. **Highlight the program name** in each phrase:
   - Select "Foundation in Science" → Choose entity `@program_name`
   - Select "Foundation in Arts" → Choose entity `@program_name`

### Step 5: Configure Parameters

1. **In the intent**, go to **"Parameters"** section
2. **Add a parameter:**
   - **Parameter name:** `program_name`
   - **Entity:** `@program_name`
   - **Value:** `$@program_name`
   - **Required:** ✅ (check this)
3. **Add another parameter:**
   - **Parameter name:** `info_type`
   - **Entity:** `@info_type` (or use a system entity)
   - **Value:** `$info_type` (or set default to "requirements")
   - **Required:** ❌ (optional)

### Step 6: Test

1. **Go to "Test" tab** in Dialogflow console
2. **Type:** "Requirements for Foundation in Science"
3. **Check the response:**
   - Should show: "Here are the admission requirements for Foundation in Science: http://172.20.10.3:5000/admission/requirements?program_id=60"
   - Should NOT show: `{@program_name}`

## Important Notes

### Priority Order
Dialogflow uses responses in this order:
1. **Webhook fulfillment** (if enabled) ← You want this!
2. **Static responses** (if webhook fails or is disabled) ← Remove these!

### If Webhook is Not Being Called

Check your Flask server logs. You should see:
```
INFO:routes.dialogflow_webhook:Dialogflow webhook received: {...}
```

If you DON'T see this, Dialogflow is not calling your webhook.

### Common Issues

1. **Static response overriding webhook:**
   - Solution: Delete all static responses

2. **Webhook not enabled:**
   - Solution: Enable "Enable webhook call for this intent"

3. **Wrong webhook URL:**
   - Solution: Check Settings → Fulfillment → Webhook URL

4. **Entity not being extracted:**
   - Solution: Add more training phrases and mark entities correctly

5. **Typo in user query (e.g., "Scienece"):**
   - Your webhook code already handles this, but Dialogflow entity extraction might fail
   - Solution: The webhook will extract from query text as fallback

## Testing Checklist

- [ ] All static responses removed from intent
- [ ] Webhook fulfillment enabled in intent
- [ ] Webhook URL configured in Settings → Fulfillment
- [ ] Entity `@program_name` created with program names
- [ ] Training phrases added with entities marked
- [ ] Parameters configured correctly
- [ ] Flask server running and accessible
- [ ] Test query works in Dialogflow console

## Debugging

If it's still not working:

1. **Check Flask logs** - Is webhook being called?
2. **Check Dialogflow logs** - Go to "History" tab, see what was sent
3. **Test webhook directly** - Use the test script: `python test_dialogflow_webhook.py`
4. **Check entity extraction** - In test console, see if `@program_name` is highlighted
