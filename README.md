# Hebrew Learning App - User Guide 🇮🇱

A desktop application for learning Hebrew vocabulary with smart flashcards, audio pronunciation, and spaced repetition.

---

## ✨ Features

### Learning System
- **30+ Hebrew words** with rich linguistic data (expandable to hundreds)
- **SQLite database** - Professional vocabulary storage with variants, categories, translations
- **15+ study modes** - Smart learning paths for different goals
- **Spaced Repetition (SRS)** - Learn efficiently with scientifically proven intervals
- **4-level confidence rating** - Again/Hard/Good/Easy
- **Progress tracking** - Track familiarity, easiness, streaks, and review dates

### Rich Vocabulary Data
- **Parts of speech** - Verbs, nouns, adjectives, prepositions
- **Hebrew roots** - See word families and etymology
- **Variants** - Plural forms, gender forms, conjugations
- **Translations** - Greek, Arabic, Russian cross-references
- **Categories** - Greetings, Biblical Hebrew, Torah, Common Words
- **Register** - Modern Hebrew, Biblical Hebrew, or both

### Audio & Interface
- **Native Hebrew audio** - macOS text-to-speech with Carmit voice
- **Dark mode** - Easy on the eyes for evening study
- **Keyboard shortcuts** - Numbers 1-4 for fast rating
- **Modern design** - Clean, distraction-free interface
- **Customizable UI** - Adjust colors, fonts, spacing (see Developer Guide)

---

## 🚀 Quick Start

### Installation
1. Double-click `HebrewLearning.app` to launch
2. First run will create the SQLite database with sample vocabulary
3. Start studying from the Study menu!

### Your First Study Session
1. **Menu: Study → Quick Start → Top 50 Words**
2. Hebrew word + transliteration appears
3. Audio plays automatically
4. Try to recall the meaning
5. Press **Space** to show the answer
6. Rate yourself: **1** (Again), **2** (Hard), **3** (Good), or **4** (Easy)

---

## 📖 Study Modes - Complete Guide

### 🚀 Quick Start
Traditional frequency-based learning

- **Top 50/100/200** - Study most common words
- **All Words** - Study entire vocabulary
- **Custom Range** - Choose specific rank range (e.g., 11-30)

**Best for:** Beginners, systematic learning

---

### 🧠 Smart Study
Intelligent learning algorithms

#### SRS Review (Due Today) ⭐ **MOST IMPORTANT**
- Shows only words scheduled for review today
- Uses spaced repetition algorithm (like Anki)
- Overdue words appear first
- **Best for:** Daily review routine

#### Learn New Words
- Studies 10 words you've never seen before
- Sorted by frequency (most common first)
- **Best for:** Expanding vocabulary gradually

#### Review Weakest Words
- Practice your 20 weakest words
- Sorted by familiarity and easiness score
- Targets words you struggle with
- **Best for:** Reinforcing difficult vocabulary

#### Review Strongest Words
- Review your 20 strongest words
- Maintains mastery
- **Best for:** Confidence building

#### Practice Difficult (Top 50/100)
- Only shows words marked "Again" or "Hard"
- Filters out words you know well
- **Best for:** Targeted problem-solving

---

### 📑 By Category
Thematic vocabulary groups

- **Greetings** - Hello, thank you, please
- **Common Words** - Most frequently used
- **Basic Vocabulary** - Essential everyday words
- **Verbs** - Action words (eat, walk, do)
- **Nouns** - Things (house, book, person)
- **Adjectives** - Descriptive words (good, big, small)
- **Biblical Hebrew** - Ancient text vocabulary
- **Torah** - Genesis-specific words
- **Prepositions** - Relationship words (of, with, on)

**Best for:** Learning related words together

---

### 🎯 By Type
Linguistic filtering

#### By Register (Time Period)
- **Modern Hebrew** - Contemporary spoken Hebrew
- **Biblical Hebrew** - Ancient/classical Hebrew
- **Both** - Words used in both contexts

#### By Part of Speech
- **Verbs Only** - All verbs (see conjugation patterns)
- **Nouns Only** - All nouns
- **Adjectives Only** - All descriptive words
- **Prepositions Only** - All relationship words

**Best for:** Grammar-focused learning, pattern recognition

---

### 🎲 Random
- **Random 10 Words** - Variety and spontaneity
- **Best for:** Quick review, testing knowledge

---

## 📊 Recommended Study Routines

### Daily Routine (15-20 minutes)
```
1. SRS Review (Due Today) - 5 min  ⭐ Most important
2. Learn New Words - 5 min
3. Review Weakest Words - 5 min
4. One category of interest - 5 min
```

### Weekly Deep Dive
```
Monday: Verbs Only
Tuesday: Nouns Only
Wednesday: Adjectives Only
Thursday: Biblical Hebrew
Friday: Review Weakest Words
Weekend: Random mix
```

### Rapid Learning (Intensive)
```
1. Learn New Words (10 words)
2. SRS Review those words later
3. Practice them by category
4. Review weakest next day
5. Repeat daily
```

---

## 💡 Understanding the Ratings

### When to Use Each Level

**Again (1)** 🔴
- Complete failure - couldn't recall at all
- Word will be shown again soon (today)
- **Use when:** You have no idea what the word means

**Hard (2)** 🟠
- Difficult - barely recalled with struggle
- Word scheduled for next day review
- **Use when:** You remembered after thinking hard, not confident

**Good (3)** 🟢
- Recalled with some effort
- Word scheduled for review in 3 days
- **Use when:** You got it right, but not instantly

**Easy (4)** ✅
- Perfect recall - instant recognition
- Word scheduled for review in 7+ days
- **Use when:** You knew it immediately, very confident

### How SRS Works
- Each word has an **easiness factor** (1.3-3.0)
- Each rating adjusts the factor and interval
- "Again" decreases easiness → more frequent reviews
- "Easy" increases easiness → longer intervals
- Your **streak** counts consecutive successful reviews

---

## ⌨️ Keyboard Shortcuts

| Action | Keys | When to Use |
|--------|------|-------------|
| Show Answer | **Space** | Reveal the English translation |
| Again | **1** or **A** | Didn't know it |
| Hard | **2** or **H** | Struggled to recall |
| Good | **3** or **G** | Got it right |
| Easy | **4** or **E** | Knew it instantly |
| Play Audio | **P** | Replay pronunciation |
| Toggle Theme | **\\** (backslash) | Switch light/dark mode |

💡 **Tip:** Keep your hand on the number keys for fastest rating!

---

## 📈 Tracking Progress

### View Statistics
**Menu: Vocabulary → View Statistics**

Shows:
- Total words in database
- Breakdown by confidence level (Easy/Good/Hard/Again)
- Percentage studied vs. not studied
- Your progress over time

### Understanding Your Progress
- **Easy (Mastered):** You've learned these well
- **Good (Confident):** On track, need occasional review
- **Hard (Struggling):** Need more practice
- **Again (Need Review):** Focus here first
- **Not Studied:** New vocabulary to learn

---

## 🎨 Customization

### Toggle Dark Mode
**Menu: Settings → Toggle Dark Mode** (or press **\\**)
- Light theme for daytime study
- Dark theme for evening/night

### Audio Settings
**Menu: Settings → Auto-play Audio**
- On: Audio plays automatically when card appears
- Off: Press **P** to play audio manually

### Import Vocabulary
**Menu: Vocabulary → Add New Words from File**

Format: Tab-separated text file
```
rank    english         transliteration    hebrew
301     hello           shalom             שלום
302     goodbye         lehitraot          להתראות
```

---

## 🏆 Pro Tips

### 1. Be Honest with Ratings
- Don't mark "Easy" if you hesitated
- Being honest helps the algorithm schedule better
- "Again" and "Hard" are not failures - they're data!

### 2. Do Daily SRS Reviews First
- Most efficient learning happens here
- Only takes 5-10 minutes
- Catches words before you forget them

### 3. Mix Study Modes
- Morning: SRS Review (maintain)
- Afternoon: Learn New Words (expand)
- Evening: By Category (contextualize)

### 4. Use Categories for Context
- Learning verbs? Study "Verbs Only" to see patterns
- Then study "Common Words" to see verbs in use
- Context helps memory!

### 5. Don't Overload
- 10 new words per day is better than 50
- Quality over quantity
- Consistent daily practice beats cramming

### 6. Study Root Families
- Notice the roots in word notes
- Words from same root are related
- Learning one helps learn others

---

## 🔧 Troubleshooting

### No Audio?
- Check System Preferences → Accessibility → Spoken Content
- Make sure Hebrew (Carmit) voice is downloaded
- Try System Preferences → Siri & Spotlight → Siri Voice

### App Won't Open?
- Right-click → Open (first time only)
- Allow in System Preferences → Security & Privacy

### Progress Not Saving?
- Check if you have write permissions to app directory
- Progress auto-saves after each word rating
- Database file: `hebrew_vocabulary.db`

### Database Issues?
- Delete `hebrew_vocabulary.db` to reset
- Restart app - it will create fresh database
- Sample data populates automatically

---

## 📚 Current Vocabulary

### Sample Database Includes:
- 30 carefully selected Hebrew words
- Mix of modern and biblical Hebrew
- Common greetings and everyday words
- Important verbs, nouns, adjectives
- Biblical terms from Genesis
- Multiple word variants and forms
- Cross-language translations

### Word Features:
- ✅ Frequency rankings
- ✅ Parts of speech labeled
- ✅ Hebrew roots provided
- ✅ Plural/gender forms
- ✅ Translations to Greek, Arabic, Russian
- ✅ Categorized by theme
- ✅ Register marked (modern/biblical/both)

---

## 🎯 Learning Goals

### Beginner (First Week)
- Complete "Learn New Words" daily
- Study "By Category → Greetings"
- Try "Quick Start → Top 50"
- **Goal:** Learn 30 words with confidence

### Intermediate (First Month)
- Do "SRS Review" every day
- Add 5-10 new words daily
- Study categories systematically
- **Goal:** 100+ words, use SRS effectively

### Advanced (Ongoing)
- Maintain daily SRS reviews
- Study by part of speech for grammar
- Learn Biblical Hebrew separately
- **Goal:** Expand to hundreds of words, high retention

---

## 📖 About the Database

Your vocabulary is stored in `hebrew_vocabulary.db` - a professional SQLite database with:

- **6 tables** - Organized relational data
- **Lemmas** - Core vocabulary entries
- **Variants** - Word forms and conjugations
- **Categories** - Thematic groupings
- **Translations** - Cross-language references
- **Progress** - Your learning data
- **Links** - Connections between all data

This structure allows powerful features:
- Filter by any property
- Track detailed progress
- Scale to thousands of words
- Fast queries and searches
- Export/import capabilities

---

## 🚀 Future Features

With the SQLite database, upcoming features could include:
- Search by Hebrew root
- Filter by multiple categories
- Custom SRS interval settings
- Statistics by category/type
- Export progress reports
- Word family clustering
- Etymology exploration
- Audio file support (for Windows)

---

## ❓ FAQ

**Q: How many words can I add?**
A: Unlimited! The database scales easily to thousands of words.

**Q: Can I share my progress?**
A: Yes, the database file `hebrew_vocabulary.db` contains everything.

**Q: Does it work offline?**
A: Yes! Everything is local, no internet needed.

**Q: Can I backup my progress?**
A: Yes, just copy `hebrew_vocabulary.db` to backup location.

**Q: Will this work on Windows?**
A: Currently macOS only. Audio uses macOS text-to-speech.

**Q: How accurate is the spaced repetition?**
A: Based on proven SRS algorithms similar to Anki/SuperMemo.

---

## 📞 Support

For issues, questions, or feature requests:
- Check the Developer Guide for customization
- Review the database with `python3 inspect_database.py`
- GitHub: HebrewLearning repository

---

## 🎓 Happy Learning!

Remember:
- **Consistency beats intensity** - 15 minutes daily > 2 hours weekly
- **Be honest with ratings** - Helps the algorithm help you
- **Use SRS Review daily** - Most efficient learning method
- **Mix study modes** - Keeps learning engaging
- **Track your progress** - Watch yourself improve!

The best way to learn is to start! Open the app and begin your Hebrew journey today. 🇮🇱

---

**Version 2.5** - Modular Architecture with SQLite Database
