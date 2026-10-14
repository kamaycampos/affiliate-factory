# THE AFFILIATE FACTORY
### Give this one file to your Claude. That's the whole instruction.

> **For you, the member: three things, then you're done reading.**
> 1. Open the **Claude app** on your computer (Mac or PC), click **Code**, and pick any folder (your Desktop is fine).
> 2. Drag this file into the message box and type: **Set me up.**
> 3. For about 30 minutes, your Claude does the work. You only **log in**, click **Allow**, and **pick what you like** from pictures.
>
> **Cost: nothing beyond your Claude Pro plan.**
>
> No Claude app yet? Download it free at **claude.ai/download** and sign in with your Claude Pro account. You'll also want the free **Claude in Chrome** extension; your Claude will show you where to get it.

---

## FOR CLAUDE: read all of this before your first message to the member

You are setting up **The Affiliate Factory** for a Kevin Trudeau affiliate. Assume they are **not technical, possibly older, and easily overwhelmed**. They will judge the whole product by how these 30 minutes *feel*. If they feel lost even once, the product failed. Your tone: warm, calm and brief, one thing at a time.

The machine lives at **github.com/kamaycampos/affiliate-factory**. Once their copy exists, its `CLAUDE.md` is your manual for every day after setup. **This file is your manual for setup.**

---

## 1. THE IDEAL SCENE: what "finished" means
Read this twice. Every decision you make serves these two targets.

### Target 1: everything runs by itself, forever
After setup, the member never has to do anything for the machine to keep working:
- **New Kevin episodes are found and cut automatically.** His newest upload is cut first, the same day it appears.
- **Every week the best moments are chosen** (a scheduled Claude routine) in the member's voice, opening on the strongest line. The first 3 seconds decide everything.
- **Clips are made in full HD**, with a six-word hook and word-perfect captions timed to Kevin's voice. Every clip passes quality gates before it can be posted.
- **Clips post themselves** to Instagram, Facebook and YouTube, spaced like a human would post them. TikTok clips arrive in drafts, ready to post with one tap.
- **Every comment with their keyword gets their link by DM**, automatically, once per person.
- **Their numbers are measured** (views, comments, DMs, clicks), and what works feeds the next week's choices.
- **They watch it all from one page**, their control panel, and they never need to open GitHub.

### Target 2: their style, defined once, easily, and theirs
Every member is different. **Their clips start plain** (white words, no colour, no effects). Within a few minutes, **by telling you in their own words or showing you examples they love** (a screenshot, a reel, a brand they admire), never by writing specs, they define:
- **the look:** caption style, colours, capitals, font feel
- **the voice:** calm teacher, bold challenger or storyteller
- **the lane:** money, real estate, manifesting, business stories, mindset (and the mix)
- **the ask:** the word viewers comment to get their link

From then on, every clip is made **their** way automatically. They can change any of it later just by telling you ("make the captions yellow", "more real estate").

### The finish line: setup is done only when every box is true
Check each one yourself before you say "done". Don't take a tool's word for it: look at the result.
- [ ] Their own copy of the factory exists in **their** GitHub, and their control panel opens in the browser
- [ ] Their brand file holds their name, voice, lane and keyword (read it back to them)
- [ ] Their style is chosen, and they have **seen** what a clip will look like
- [ ] Instagram, Facebook and YouTube post automatically; TikTok drafts arrive ready to tap
- [ ] Comment → DM answers their keyword (prove it: comment the keyword from a second account and watch the DM arrive)
- [ ] The first factory run has started (the first clips arrive in 1–3 hours)
- [ ] The weekly planning routine exists on their Claude account
- [ ] You told them, in **three lines**, what happens next and the one page they can look at

---

## 2. HOW YOU WORK WITH THEM (non-negotiable)
1. **Show, don't tell.** Before every step, open the visual guide card for that step: **kamaycampos.github.io/affiliate-factory/start/**. Or take a screenshot of the exact screen and say where to click ("the green button, top right"). Never send them to read a document.
2. **One step per message.** Say what's about to happen in one sentence, do it, and confirm it worked in one sentence. Show a progress bar like `Step 3 of 7 ▓▓▓░░░░`.
3. **They only do three kinds of things:** log in (they type their own passwords; **you never type a password, code or card number**), click **Allow / Continue / Approve**, and choose. Everything else is yours.
4. **You drive their Chrome** with Claude in Chrome. Ask once at the start: *"May I use your Chrome to set everything up? You'll approve each log-in."* If Claude in Chrome isn't connected, help them install it first (step 0). It's the difference between 30 minutes and 3 hours.
5. **Never paste a key, token or password into the chat.** Secrets go straight into GitHub's secret settings, by you, in their browser.
6. **Watch the clock.** Each step below has a time budget. If a step runs over by 5 minutes, stop, say plainly what's blocking, offer the simplest way around it, and keep going.
7. **Never leave them on a dead end.** If something can't be done today (an app approval, a waiting period), say exactly what happens instead and when. Then move on.

---

## 3. THE RUN: 7 steps, about 30 minutes of their time
`[You]` = you do it. `[Them]` = they do it. Open the matching card of the visual guide at each step.

### Step 0: Ready check (2 min)
- `[You]` Confirm you're in the Claude app's **Code** tab on their computer, and that Claude in Chrome is connected.
- If Claude in Chrome isn't connected: send them **chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn**. `[Them]` click **Add to Chrome**, then sign in.
- `[Them]` Have ready: their KT affiliate link (from the affiliate portal), and the logins for their Instagram, Facebook, YouTube and TikTok.

### Step 1: Their own factory (4 min) · *Card 1*
- `[You]` Open github.com. If they have no account: `[Them]` sign up (their email, their password); you fill everything else.
- `[You]` Open **github.com/kamaycampos/affiliate-factory** → **Use this template → Create a new repository**. Name it `my-factory`, keep it **Public** (free, and their videos are stored encrypted) → **Create**.
- `[You]` Clone it into the folder you're working in, then read its `CLAUDE.md`. From now on, follow that file's `start` section **in the order and style of this document**.

### Step 2: The keys and the control panel (3 min) · *Card 2*
- `[You]` Run `python3 personalize.py`. Put `FACTORY_KEY`, `TRANSCRIPT_KEY` and `OFFER_URL` (their affiliate link) into **Settings → Secrets and variables → Actions**, yourself, in their browser.
- `[You]` Turn on **Settings → Pages → Deploy from a branch → main / docs**.
- `[You]` Tell them: *"Your factory has its own page now. I'll open it for you at the end."*

### Step 3: Their style, from pictures (5 min) · *Card 3*
Ask **one question at a time**, always with **pictures or examples** to choose from:
1. **"How do you want your clips to look?"** Their clips start **plain** (the default in `my_brand/style.json`). Ask them to **tell you or show you**: colours they love, their brand or logo, a screenshot or a reel whose look they want. Never hand them a menu of presets. Turn what they say into `my_brand/style.json` (colours, hook card colour, case, shadow, font; see the `style` section of `CLAUDE.md`), render **one preview frame** with their colours, and show it. Adjust until they say "yes, that's me".
2. **"How should you sound?"** Calm teacher / bold challenger / storyteller. Read one example caption in each voice, then let them pick.
3. **"What should your clips be about?"** Show the lanes with one real hook each (money: *"The 30% rule every wealthy person follows"*; real estate: *"How rich people actually buy houses"*; manifesting: *"$1 million before he turned 18"*). Ask for a rough mix.
4. **"What word should people comment to get your link?"** Suggest **MONEY** or **BRAIN**, the two strongest measured.
5. Their name and handles. Read them off their profiles yourself when you're logged in.

`[You]` Write `my_brand/BRAND.md`. Read it back in **five short lines** and ask *"Anything to change?"*

### Step 4: Connect the platforms (15 min) · *Card 4*
**Everything here is free. Their only cost is Claude Pro.** Do it in this order:
- **Instagram + Facebook (one Meta setup covers both):** follow `SETUP_META.md` yourself, in their Chrome (Meta app, Page token). `[Them]` click **Continue as…** and **Allow**. From then on, both post by themselves.
- **YouTube:** follow the YouTube part of `SETUP_POSTING.md` yourself (Google Cloud project, YouTube Data API, consent screen **published to Production**, token). `[Them]` click **Allow**. YouTube then posts by itself. If Google ever keeps a new project's uploads private, fill in Google's free YouTube API review form with them; until it passes, those clips are one tap from the panel.
- **TikTok:** clips arrive in their **TikTok drafts** with the caption ready, and they tap **Post**. TikTok doesn't approve personal posting apps yet. Tell them plainly that this is the one tap that stays.

Then `[You]` set the repository **variable** `AUTOPOST` = `on`, and the secret `KT_PLATFORMS` = the platforms you connected (e.g. `instagram,facebook,youtube,tiktok`).

### Step 5: Comment → DM, their link sent automatically (5 min) · *Card 5*
**Meta's own rule is the way: it answers in seconds, publicly and by DM.** Set it up first, always.
- `[You]` Open **business.facebook.com → Inbox → Automations → Create automation → Comment to message**. It's built into Meta, free, and needs no app.
  - Channels: Instagram and Facebook
  - Keywords: their word, in capitals and lowercase (e.g. `MONEY`, `money`)
  - Private message: *"Here it is: {their link} - #ad, I earn a commission if you buy through my link."*
  - Public reply: *"Just sent it to you - check your messages"*
  - Save, then **reload the page** and confirm the rule shows as ON.
- **Backup only:** if Meta's rule stays silent (it can stop if Meta ever restricts the Page), turn the rule OFF and switch on the factory's own DM bot (`DM_AUTO` = `on`; the Page token needs `pages_messaging` and `instagram_manage_messages`). It answers within minutes, not seconds. **Use one system, never both**, or people get two DMs.
- **Prove it:** ask them to comment the keyword from another account (a friend or a second profile) on any post, and watch the DM arrive together. If it doesn't arrive in 2 minutes, say exactly why. Don't leave it.

### Step 6: Switch it on, and the weekly brain (2 min) · *Card 6*
- `[You]` Start their first factory run: **Actions → factory → Run workflow**. The first clips arrive in 1–3 hours.
- `[You]` Create a **weekly scheduled routine** on their Claude account (Monday morning, their time) on this repository, with the prompt `plan, then report`. If routines aren't available on their plan, tell them the one sentence that replaces it: say **plan** once a week.

### Step 7: The finish line (1 min) · *Card 7*
- `[You]` Tick every box of **THE IDEAL SCENE** above, checking each result yourself.
- `[You]` Open their control panel (`https://THEIR-NAME.github.io/my-factory/`) in their browser.
- `[You]` Tell them in three lines:
  1. *"Your first clips arrive in a few hours, and they post by themselves."*
  2. *"Everything is on this page; bookmark it."*
  3. *"Want a change? Just tell me in plain words: 'more real estate', 'yellow captions', 'post 3 a day'."*

---

## 4. RULES THAT PROTECT THEIR ACCOUNTS
- **Affiliate disclosure** on every DM and wherever a link appears (`#ad`). No promises about health or income. Their Claude enforces `playbook/COMPLIANCE.md` on every clip.
- **Captions stay a little careful** with words platform filters flag (guaranteed, miracle, cure, free money, risk-free, DM me). The factory softens them automatically. Don't fight it.
- **One ask per post:** one question and one keyword line, never two questions.
- **Only Kevin's authorised footage**, only **1080p or better**, and the newest upload is always cut first.

## 5. WHAT THEY SAY AFTER SETUP (plain words work too)
| They say | You do |
|---|---|
| `plan` | Choose this week's clips (the routine already does this weekly) |
| `clips` | Show what was made, with captions |
| `report` | What won, what lost, what to change, in three lines |
| `style` | Change the look by talking ("bigger captions", "no capitals") |
| `teach` | They show a reel they love; the next clips learn from it |
| `money` | Read their affiliate portal with them and update their numbers |
| `update` | Get the newest version of the factory, keeping everything that's theirs |

## 6. IF SOMETHING BLOCKS
- **A platform refuses a login or asks for a phone code:** they enter it; you wait. Never ask them to read you a code.
- **Meta asks to verify the Page or the person:** they do it on their phone; you continue with the next step meanwhile.
- **Anything takes more than 5 minutes extra:** say what it is, give the simplest workaround, and keep the finish line in sight.

*Built and proven on a live account first: 214,805 views on one reel, 6 posts a day across four platforms, no servers.*
