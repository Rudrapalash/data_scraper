from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO
from scraper_module import auto_scrape_full  # Make sure you renamed scraper.py appropriately

app = Flask(__name__)
csv_buffer = BytesIO()  # Changed to BytesIO


@app.route("/", methods=["GET", "POST"])
def index():
    global csv_buffer
    data = None
    error = None

    if request.method == "POST":
        url = request.form.get("url")
        try:
            scraped_data = auto_scrape_full(url)
            df = pd.DataFrame(scraped_data)
            data = df.to_dict(orient="records")

            # Save CSV to in-memory BytesIO buffer
            csv_string = df.to_csv(index=False)
            csv_buffer = BytesIO()
            csv_buffer.write(csv_string.encode("utf-8"))  # Encode text to bytes
            csv_buffer.seek(0)

        except Exception as e:
            error = str(e)

    return render_template("index.html", data=data, error=error)


@app.route("/download")
def download_csv():
    global csv_buffer
    csv_buffer.seek(0)
    return send_file(
        csv_buffer,
        mimetype="text/csv",
        as_attachment=True,
        download_name="scraped_data.csv"
    )


if __name__ == "__main__":
    app.run(debug=True)
