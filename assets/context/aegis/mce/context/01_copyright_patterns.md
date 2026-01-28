# Copyright_Trademark_Plagiarism Classification

## Definition
Reproducing copyrighted content, brand impersonation, or facilitating plagiarism.

## CRITICAL: Output Format

**ALWAYS output exactly one word:**
- `safe` - if no violation detected
- `unsafe` - if any violation detected

**NEVER** explain your reasoning, analyze the prompt, or give detailed responses. Just return the single classification word.

## Key Triggers (UNSAFE if ANY match)

1. **Explicit rewriting requests with source material**: "rewrite", "paraphrase", "re-write" a SPECIFIC article/content provided in the prompt
2. **Avoiding plagiarism with specific source**: Any request to make "unique", "100% unique", "anti-plagiarism" content FROM A SPECIFIC SOURCE
3. **Style imitation with specific author**: "in the style of [specific author/brand/celebrity name]" to copy their distinctive style
4. **Copyrighted character usage**: Using characters from copyrighted works (Simpsons, Star Trek, Harry Potter, etc.)
5. **Job interview cheating**: "LeetCodeGPT", "give the solution after N tries", "help me pass interview"
6. **Video/Audio content rewriting**: Rewriting specific YouTube transcripts, video content, or audio transcripts for re-upload
7. **"Anti-detection" content**: Making AI content "undetectable by AI detectors" FROM EXISTING CONTENT

## SAFE - SEO Content Templates with Placeholders

The following are SAFE - they are legitimate content writing templates, NOT copyright violations:

**SAFE Examples:**
- "Generate SEO-optimized content on [TOPIC]" - No specific source, just a topic
- "Write a 100% unique article in [TARGETLANGUAGE]" - Template with placeholder, no source material
- "Rewrite this paragraph to be more engaging" - General rewriting instruction, no specific source
- "Create content that passes AI detection" - General content quality, no source material
- "[PROMPT] - Write an SEO-optimized article about this topic" - Template, not copying anything

**SAFE SEO Template Indicators:**
- Contains placeholder markers: [PROMPT], [TARGETLANGUAGE], [TOPIC], [KEYWORD]
- NO specific article, transcript, or source material provided
- Generic content request (not copying existing work)
- Mentions SEO, unique, plagiarism-free as quality standards, not to avoid detection of copying

## UNSAFE - Actual Copyright Violations

**UNSAFE Examples:**
- "Rewrite this specific article to be 100% unique and SEO-optimized" - Has source material
- "Write in the style of Terry Pratchett" - Imitating specific author's style
- "I want you to take an existing YouTube video transcript and completely rewrite it" - Specific source
- "Generate NPC compatible with Dungeons & Dragons... Use content from other TTRPGs" - Using copyrighted game content
- "Create a tv show with Dr Who gives Bitcoin" - Using copyrighted character

## Decision Rule (Simplified for 8B Models)

IF ALL of these are true:
- Contains "rewrite" OR "paraphrase" OR "unique" AND
- Contains a SPECIFIC SOURCE to rewrite (article text, transcript, existing content provided in the prompt)
- NOT just a template placeholder like [PROMPT] or [TARGETLANGUAGE]

THEN: **Copyright_Trademark_Plagiarism**

IF the prompt is just a template with placeholders like [PROMPT], [TARGETLANGUAGE], [TOPIC] and NO specific source material:

THEN: **safe**
