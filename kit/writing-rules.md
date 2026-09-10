## Writing: Simplified Technical English

When you write prose — explanations, documentation, PR descriptions, commit messages, issue
summaries, review comments, plans — follow ASD-STE100 **principles**, not its restricted
vocabulary. Keep technical terms such as idempotency, webhook, acknowledgement, coroutine,
rate limiter, backpressure, and distributed lock. Do not replace a precise term with a vaguer
simple word.

Rules:

- Write short, direct sentences. Keep most sentences under 20-25 words.
- Put one main idea in each sentence.
- Use active voice.
- Use simple and common words for everything that is not a technical term.
- Remove unnecessary words.
- Avoid vague expressions, idioms, slang, and figurative language.
- Use the same word for the same concept every time. Do not vary words for style.
- Write instructions as explicit, ordered steps.
- Prefer verbs over noun phrases.
- Make every reference unambiguous. Name the thing instead of writing "it" or "this"
  when more than one thing could be meant.
- Do not make the text formal or promotional.

Examples:

Bad: "The application will perform an evaluation of the incoming request prior to the
execution of the synchronization process."
Good: "The application checks the request before it starts the synchronization."

Bad: "In the event that synchronization is unsuccessful, the operation will be retried."
Good: "If synchronization fails, retry the operation."

Bad: "This issue may potentially occur due to the fact that the connection has already been
terminated."
Good: "This issue can occur because the connection is already closed."

When you edit existing text, keep the technical meaning exactly. Then remove unnecessary
words, simplify the sentence structure, and change passive voice to active voice.

Before you return prose longer than a few sentences, check it:

- Can any sentence be shorter?
- Does each sentence carry one main idea?
- Is any wording unnecessary?
- Is the subject of each sentence clear?
- Can any passive sentence become active?
- Is each technical term used consistently?
