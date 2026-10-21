# Sales Performance Dashboard

An interactive dashboard for exploring sales, profit, order volume, and revenue trends. Use the sidebar filters to focus the KPIs and charts on a date range, product categories, regions, and a minimum sale value.

## Project objective

Present sales performance in a clear, easy-to-explore format. The dashboard summarizes the selected sales records and provides interactive charts for comparing categories, tracking monthly revenue, and exploring the relationship between sales and profit.

## Features

- Date range, category, region, and minimum sales filters in the sidebar.
- Five KPIs that update with the selected filters:
  - Total Revenue
  - Total Profit
  - Profit Margin
  - Units Sold
  - Average Order Value
- Interactive Plotly charts for revenue by category, monthly revenue, and sales versus profit.
- Currency and percentage formatting, chart hover details, and a friendly message when no records match.

## Technology stack

- Python
- Streamlit
- Pandas
- Plotly Express

## Project structure

```text
CodeNova_Task_3/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── sales.csv
```

Keep `data/sales.csv` in the `data` folder next to `app.py`. The app resolves the dataset path from the location of `app.py`, so it can find the CSV whether you launch from this folder or from the repository root.

## Install and run locally

The following commands are for Windows PowerShell. Open a terminal in the `CodeNova_Task_3` folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints a local address (usually `http://localhost:8501`) in the terminal. Open that address in a browser. If PowerShell blocks activation, use `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\streamlit.exe run app.py` instead.

If you launch from the repository root instead, run:

```powershell
streamlit run CodeNova_Task_3/app.py
```

## Using the filters

1. Choose the start and end dates with **Select date range**.
2. Select one or more categories and regions. Clear a multiselect to test the no-matching-records message.
3. Adjust **Minimum sales value** to exclude orders below the selected amount.
4. The KPIs and charts refresh when a filter changes. Hover over chart marks for more detail; Plotly charts also support zooming and panning.
5. To restore the full view, select the full date range and all categories and regions, and move the sales threshold to its minimum.

## Deploy to Streamlit Community Cloud

The dashboard has not been deployed yet. You must publish the project and create the app in Streamlit Community Cloud to receive a live URL.

1. Make sure `CodeNova_Task_3/app.py`, `CodeNova_Task_3/requirements.txt`, and `CodeNova_Task_3/data/sales.csv` are present in the GitHub repository. Commit and push the project files if they are not there yet.
2. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub and select **Create app**.
3. Select the repository and branch containing the project.
4. Set the **Main file path** to `CodeNova_Task_3/app.py` when the selected repository's root is the parent folder of `CodeNova_Task_3`. If you publish the contents of `CodeNova_Task_3` as the repository root, use `app.py` instead.
5. Deploy the app. Check the deployment logs if the build fails; confirm that the dependency file and CSV are included at the paths shown above.
6. Open the deployed app and complete the pre-deployment checklist below.
7. Copy the URL provided by Streamlit Community Cloud into the live dashboard section.

The app does not require API keys or other secrets. Its CSV path is built from the app file's location rather than a machine-specific absolute path.

## Live dashboard

**Live link:** Not deployed yet. Add the URL from Streamlit Community Cloud here after you deploy the app.

## Video or GIF walkthrough

Record a short walkthrough after running the dashboard locally or opening the deployed app. Show the initial dashboard, change at least one filter so the KPIs and charts update, and briefly point out the chart hover details. Do not include private information in the recording.

For example, use [ScreenToGif](https://www.screentogif.com/) to capture and save a short GIF, or use a screen recorder such as OBS Studio to make a video. Save the finished recording in a new `media` folder alongside this README:

```text
CodeNova_Task_3/
└── media/
    └── dashboard-walkthrough.gif
```

Once you have added the GIF to the repository, replace this note with an embedded preview:

```markdown
![Sales dashboard walkthrough](media/dashboard-walkthrough.gif)
```

For a video file, add a link to its repository path or to a shareable video page that you have published. No recording is included yet.

## Pre-deployment test checklist

- [ ] The app opens and displays the dashboard without a traceback.
- [ ] Changing the date range changes the displayed data.
- [ ] Selecting one category or region updates all five KPIs and all three charts.
- [ ] The minimum sales slider filters the records and updates the KPIs and charts.
- [ ] Clearing the category selection shows the friendly no-records message and no charts, without an exception.
- [ ] Revenue and profit are displayed as currency; profit margin is displayed as a percentage.
- [ ] Chart hover details, zooming, and the scatter plot category legend work.
- [ ] The layout remains usable in a narrow browser window.
- [ ] The deployed app can load `CodeNova_Task_3/data/sales.csv` from the repository without any local machine paths.
- [ ] The live link and walkthrough section are updated only after you publish the app and record the walkthrough.
