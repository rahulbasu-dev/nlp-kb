# NLP Classroom - Web Application

A comprehensive, scalable Flask web application for teaching Natural Language Processing concepts, featuring interactive demos, visualizations, and classroom modes.

## Quick Start (30 seconds)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
Open your browser and go to: **http://localhost:5000**

## Features

✨ **Interactive Learning**
- TF-IDF and SGNS explanations with visualizations
- Interactive demos where students can input their own text
- 11 professional visualizations for classroom use
- 9 code examples with live execution

🎓 **Classroom Ready**
- Full-screen presentation mode with keyboard controls
- 3 pre-built lesson plans (15, 30, 60 minutes)
- Pedagogically ordered curriculum
- Perfect for professors and instructors

🚀 **Scalable Architecture**
- Modular route structure - easy to add new lessons
- Template inheritance for consistent UI
- Separate static files (CSS/JS) for maintainability
- API endpoints for programmatic access

## Project Structure

```
nlp-classroom/
├── app.py                      # Main Flask application
├── sgns.py                     # SGNS and TF-IDF implementations
├── classroom_examples.py       # 9 interactive examples
├── requirements.txt            # Python dependencies
├── templates/                  # HTML templates
│   ├── base.html              # Master template with navigation
│   ├── index.html             # Homepage
│   ├── lesson_tfidf.html      # TF-IDF lesson
│   ├── lesson_sgns.html       # SGNS lesson
│   ├── lesson_comparison.html # Comparison lesson
│   ├── demo_tfidf.html        # TF-IDF interactive demo
│   ├── demo_sgns.html         # SGNS interactive demo
│   ├── visualizations.html    # Visualization gallery
│   ├── examples.html          # Code examples list
│   ├── example_detail.html    # Individual example viewer
│   ├── documentation.html     # Documentation hub
│   ├── doc_viewer.html        # Documentation viewer
│   ├── classroom.html         # Classroom mode launcher
│   └── classroom_lesson.html  # Fullscreen presentation
├── static/
│   ├── css/
│   │   └── style.css          # Custom styling
│   ├── js/
│   │   └── main.js            # Client-side interactivity
│   └── visualizations/        # PNG visualization files
│       ├── 01_tfidf_matrix.png
│       ├── 02_idf_distribution.png
│       ├── 03_tfidf_similarities.png
│       ├── 04_sgns_vs_tfidf_comparison.png
│       ├── 05_context_window.png
│       ├── 06_sampling_process.png
│       ├── 07_embeddings_2d.png
│       ├── 08_similarity_heatmap.png
│       ├── 09_algorithm_steps.png
│       ├── 10_training_dynamics.png
│       └── 11_infographic_sgns.png
└── [documentation files]
    ├── START_HERE.md
    ├── TEACHING_CHEATSHEET.md
    ├── VISUALIZATION_GUIDE.md
    ├── TEACHING_ORDER.md
    └── ONE_PAGE_SUMMARY.md
```

## Main Routes

### Learning Pages
- `/` - Home with learning path
- `/lessons/tfidf` - TF-IDF lesson with visualizations
- `/lessons/sgns` - SGNS lesson with visualizations
- `/lessons/comparison` - Side-by-side comparison

### Interactive Demos
- `/demo/tfidf` - Run TF-IDF on your own documents
- `/demo/sgns` - Train SGNS on your own corpus

### Resources
- `/visualizations` - Gallery of all 11 visualizations
- `/examples` - 9 interactive code examples
- `/docs` - Documentation hub
- `/docs/<filename>` - View specific documentation

### Classroom Mode
- `/classroom` - Select lesson plan (15/30/60 min)
- `/classroom/lesson/<type>` - Full-screen presentation mode

### API
- `GET /api/available-visualizations` - List all visualization files
- `POST /api/generate-visualizations` - Regenerate visualizations

## Keyboard Shortcuts

### In Classroom Mode
- **→ / Space** - Next slide
- **← / Backspace** - Previous slide
- **F** - Toggle fullscreen
- **Esc** - Exit classroom mode

### Code Examples
- **Copy button** - Copy output to clipboard

## For Instructors

### Adding New Lessons

1. Create a new lesson function in `sgns.py`
2. Add a new route in `app.py`:
   ```python
   @app.route('/lessons/your-lesson')
   def lesson_your_lesson():
       return render_template('lesson_your_lesson.html')
   ```
3. Create `templates/lesson_your_lesson.html` extending `base.html`

### Adding New Visualizations

1. Generate PNG files and place them in `static/visualizations/`
2. Update the visualization lists in `lesson_*` routes
3. Files are auto-discovered by the gallery

### Adding New Examples

1. Create example function in `classroom_examples.py`
2. Add to the `example_funcs` dict in `app.py`
3. Update examples list in `examples_list()` route

## Technical Stack

**Backend:**
- Flask 2.3+ (Python web framework)
- NumPy (numerical computing)
- scikit-learn (ML algorithms)
- Matplotlib & Seaborn (visualizations)

**Frontend:**
- Bootstrap 5 (responsive UI)
- Font Awesome (icons)
- Highlight.js (syntax highlighting)
- Vanilla JavaScript (interactivity)

## System Requirements

- Python 3.7+
- ~200MB disk space for visualizations
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Deployment

### Local Development
```bash
python app.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn app:app
```

### Docker (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## Troubleshooting

**Visualizations not showing?**
- Ensure PNG files are in `static/visualizations/`
- Check that filenames match exactly in routes

**Demos not working?**
- Verify SGNS and TFIDF classes are imported correctly from `sgns.py`
- Check browser console for JavaScript errors

**Port 5000 already in use?**
- Change port: `app.run(port=5001)`

## Contributing

To extend this application:
1. Follow the MVC pattern (routes in app.py, templates in templates/)
2. Use template inheritance from `base.html`
3. Add modular JavaScript functions in `main.js`
4. Keep CSS organized by component

## License

Educational material for teaching NLP concepts.

## Support

For questions or issues:
1. Check the documentation files
2. Review code examples
3. Examine existing lesson implementations

---

**Happy Teaching! 🚀**

Built with Flask, NumPy, and educational enthusiasm.
