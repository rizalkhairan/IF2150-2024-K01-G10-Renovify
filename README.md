# IF2150-2024-K01-G10-Renovify
<br />
<div align="center">
    <img src="./img/renovify.png" style="width: 800px">
</div>

<h3 align="center">Renovify</h3>


<br/>
<br/>
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#description">Description</a>
    </li>
    <li>
      <a href="#features">Features</a>
    </li>
    <li>
      <a href="#project-structure">Project Structure</a>
    </li>
    <li>
      <a href="#how-to-use">How to Use</a>
    </li>
    <li>
      <a href="#contributor">Contributor</a>
    </li>
  </ol>
</details>
<br/>

### Description
Renovify is an application implemented in Python that help users to organize house renovation plan. This application can store renovation project details, record expenses, display renovation timelines, and even collect renovation project inspirations discovered by users.


### Features

* Project
* Task
* Budget
* Timeline
* Inspiration

### Project Structure
```ssh
.
├── doc
│   ├── inspiration_edit.png
│   ├── inspiration_menu.png
│   ├── inspiration_menu_empty.png
│   ├── inspiration_menu_pages.png
│   ├── project_details_page.png
│   ├── project_filter_page.png
│   ├── project_form.png
│   ├── project_menu.png
│   ├── project_menu_empty.png
│   ├── task.png
│   ├── timeline_date_detail.png
│   ├── timeline_display.png
│   └── welcome_screen.png
├── img
│   ├── logo.jpg
│   ├── penico.png
│   ├── plusico.png
│   ├── renofivy.png
│   └── trashico.png
├── src
│   ├── budget
│   │   └── budget.py
│   ├── database
│   │   └── database.py
│   ├── inspiration
│   │   ├── Inspiration.py
│   │   ├── InspirationController.py
│   │   ├── InspirationForm.py
│   │   └── InspirationList.py
│   ├── project
│   │   ├── main.py
│   │   ├── project.py
│   │   ├── project_controller.py
│   │   ├── project_filter.py
│   │   ├── project_form.py
│   │   ├── project_list.py
│   │   └── utility.py
│   ├── task
│   │   ├── task.py
│   │   └── tes.py
│   ├── timeline
│   │   └── timeline.py
│   └── main.py
├── .gitignore
├── README.md
├── renovify.py
└── requirements.txt
```

### How to Use

1. Create a virtual environment:
   ```bash
   python -m venv venv
2. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
3. Install the dependencies:
   ```bash
   python -m pip install -r requirements.txt
4. Run the application:
   ```bash
   python renovify.py

### Contributor
| NIM | Name 
| :---: | :---: 
| 13523007 | Ranashahira Reztaputri | 
| 13523035 | M. Rayhan Farrukh | 
| 13523041 | Hanif Kalyana Aditya | 
| 13523063 | Syahrizal Bani Khairan | 
| 13523081 | Jethro Jens Norbert Simatupang | 
