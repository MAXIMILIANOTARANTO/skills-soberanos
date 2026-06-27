# Common Workflows - Vercel Specialist

## 1. Deploy a single-file functional app (from funcional-webapp-creator)

**Typical flow:**

1. User asks to create an app → Use `funcional-webapp-creator`.
2. Once the app is generated (usually a single `index.html` or small folder), prepare it for Vercel.
3. Use `vercel-specialist` to:
   - List existing projects (`vercel___list_projects`) to see if there's already a project for this app.
   - If new project needed, guide the user to create it in Vercel dashboard (or use deployment tool if available).
   - Deploy the app (`vercel___deploy_to_vercel` if the context allows, or instruct how to link the folder/repo).
   - Get the deployment URL.
   - (Optional) Set up custom domain or environment variables.

**Tips for single-file apps:**
- Vercel handles static single-file HTML extremely well.
- For apps that need environment variables (e.g., Gemini API key in RadarUsados), add them in the Vercel dashboard under Project Settings → Environment Variables.
- Enable "Automatic Git deploys" if the app is in a GitHub repo.

## 2. Review logs of a failing deployment

1. Get the Project ID and Deployment ID.
2. Use `vercel___get_runtime_logs` with filters (level: error, since: recent time).
3. Analyze the logs and suggest fixes.

## 3. Get access to a protected preview deployment

If a deployment URL returns 403:
- Use `vercel___get_access_to_vercel_url` to generate a temporary shareable link.
- Or use `vercel___web_fetch_vercel_url` if you need to fetch content programmatically.

## 4. Integrate with ecosistema-orchestrator

When `ecosistema-orchestrator` detects that a new app was created or that deployment is needed, it can recommend or call `vercel-specialist` with context like:
- "Deploy the recently created RadarUsados app to Vercel with production environment variables."

## 5. Best practices recommended by this skill

- Always prefer **Preview Deployments** for testing.
- Use **Environment Variables** in Vercel dashboard (never commit secrets).
- For apps with API keys (like Gemini), add them as `GEMINI_API_KEY` in Vercel.
- Monitor with `vercel___get_runtime_logs` after important deployments.
- Consider connecting the GitHub repo for automatic deploys.

This skill makes deployment a natural extension of the app creation flow in the ecosystem.