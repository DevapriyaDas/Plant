# -*- coding: utf-8 -*-
"""project plant.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NF79NM3MCoKExMTUs48ZCUOKVu2Prskh
"""

pip install rasterio

pip install earthpy

pip install scikit-learn

pip install seaborn

name=input("Enter name: ")
email_id=input("Enter email id: ")
language= input("Enter English or Hindi: ")

import rasterio as rio
import numpy as np
import earthpy.plot as ep
import earthpy.spatial as es
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


image_path = "/content/img1.jpg"
# Open the image
with rio.open(image_path) as src:
    # Reading bands (assuming multi-band image)
    red = src.read(1)
    green = src.read(2)
    blue = src.read(3)

def calculate_band_stats(band):
    """Calculate statistics for the given band."""
    return {
        'mean': np.mean(band),
        'median': np.median(band),
        'std': np.std(band),
        'min': np.min(band),
        'max': np.max(band),
    }

# Calculate stats for each band
red_stats = calculate_band_stats(red)
green_stats = calculate_band_stats(green)
blue_stats = calculate_band_stats(blue)

import matplotlib.pyplot as plt

# Global counter variable to keep track of the number of times the function is called
hist_counter = 0

def plot_histogram(band, title):
    global hist_counter  # Declare the counter as global to modify its value
    hist_counter += 1    # Increment the counter each time the function is called

    plt.figure(figsize=(10, 4))
    plt.hist(band.ravel(), bins=256, color='gray', alpha=0.7)
    plt.title(title)
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')

    # Save the histogram with a dynamic filename
    plt.savefig(f'hist{hist_counter}.png', dpi=300)  # Save as hist1.png, hist2.png, etc.
    plt.show()

# Plot histograms for each band
plot_histogram(red, 'Red Band Histogram')
plot_histogram(green, 'Green Band Histogram')
plot_histogram(blue, 'Blue Band Histogram')



def linear_stretch(image):
    """Perform linear stretching of the image."""
    p2, p98 = np.percentile(image, (2, 98))
    stretched = np.clip((image - p2) / (p98 - p2), 0, 1)
    return stretched
stretched_green = linear_stretch(green)

# Display the stretched band
plt.imshow(stretched_green, cmap='gray')
plt.title('Green Band with Linear Stretch')
plt.colorbar()
plt.savefig('linearstretch.png', dpi=300)
plt.show()


from sklearn.cluster import KMeans

# Flatten the bands and perform K-means clustering
pixels = np.dstack([red, green, blue]).reshape(-1, 3)
kmeans = KMeans(n_clusters=3).fit(pixels)
segmented_image = kmeans.labels_.reshape(red.shape)

# Plot segmented image
plt.imshow(segmented_image, cmap='tab20')
plt.colorbar(label='Segment')
plt.title('Image Segmentation using K-means')
plt.savefig('kmeanscluster.png', dpi=300)
plt.show()

def categorize_pixels_by_range(image):
    """Categorize pixel values into specified ranges and return a DataFrame."""
    # Define the new bins and labels for -1 to 1
    bins = [0, 0.5, 0.665, 0.83, 1]
    labels = ['Dead plant', 'Unhealthy plant', 'Moderately healthy plant', 'Very Healthy plant']

    # Flatten the image array and categorize into bins
    pixel_values_flat = image.flatten()
    categorized_pixels = pd.cut(pixel_values_flat, bins=bins, labels=labels, include_lowest=True)

    # Create an empty DataFrame with columns representing the pixel ranges
    categorized_df = pd.DataFrame({label: [] for label in labels})

    # Populate the DataFrame by appending pixels to the corresponding bin
    for label in labels:
        # Extract the pixel values belonging to the current range
        pixels_in_range = pixel_values_flat[categorized_pixels == label]

        # Append the pixel values as a column
        categorized_df[label] = pd.Series(pixels_in_range)

    return categorized_df

stretched_green = linear_stretch(green)

# Categorize the pixel values and convert to DataFrame format
pixel_categorized_df = categorize_pixels_by_range(stretched_green)

# Save the DataFrame to CSV
pixel_categorized_df.to_csv('pixel.csv', index=False)

print("CSV file with pixel values categorized by range saved.")

# Step 2: Import required libraries
import pandas as pd
import matplotlib.pyplot as plt

# Step 3: Load the CSV file into a DataFrame
df = pd.read_csv('/content/pixel.csv')

# Step 4: Check the DataFrame (optional)
print(df.head())
df_sum = df.sum()  # Sum of each column

# Step 6: Plotting the pie chart
plt.figure(figsize=(10, 8))
plt.pie(df_sum, labels=df_sum.index, autopct='%1.1f%%', startangle=140)
plt.title('Categorized Pixel Values Distribution')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.savefig('/content/piechart.png', dpi=300)
plt.show()
print("Piechart saved as an image.")

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

# Load your data
df = pd.read_csv('/content/pixel.csv')

# Calculate descriptive statistics
stats = df.describe()

# Create a figure and axis for the plot
fig, ax = plt.subplots(figsize=(8, 4))  # Set the figure size

# Hide the axes
ax.axis('off')

# Create the table
tbl = table(ax, stats, loc='center', cellLoc='center', colWidths=[0.2] * len(stats.columns))

# Style the table (optional)
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1.6, 1.6)  # Scale the table for better visibility
# Show the plot (optional)
plt.show()

# Save the table as an image
plt.savefig('/content/descriptive_statistics_table.png', dpi=300)
print("Descriptive statistics table saved as an image.")

import seaborn as sns
plt.figure(figsize=(10, 6))
sns.boxplot(data=df)
plt.title('Box Plot of Plant Health Categories')
plt.ylabel('Health Score')
plt.savefig('boxplot_img.png', dpi=300)
plt.show()
print("Boxplot saved as an image.")

pip install reportlab

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as PDFImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch  # Import inch for sizing

# Define the PDF file path
pdf_path = '/content/plant_analysis.pdf'

# Function to create the PDF
def create_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create a list for elements
    elements = []

    # Title of the PDF
    title = Paragraph("Analysis obtained from the plant land image", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))  # Add space after title

    # Section 1: Red Green Blue Bands
    section1_title = Paragraph("Section 1: Red Green Blue Bands", styles['Heading2'])
    elements.append(section1_title)
    elements.append(Spacer(1, 12))

    # List of RGB images (5 images)
    rgb_images = ['/content/kmeanscluster.png', '/content/linearstretch.png',
                  '/content/hist1.png', '/content/hist2.png',
                  '/content/hist3.png']

    # Add images to the first section
    for image_path in rgb_images:
        img = PDFImage(image_path)
        img.drawHeight = 3 * inch  # Set height
        img.drawWidth = 3 * inch  # Set width
        elements.append(img)
        elements.append(Spacer(1, 10))  # Space between images

    # Section 2: Plant Health Data
    section2_title = Paragraph("Section 2: Plant Health Data", styles['Heading2'])
    elements.append(section2_title)
    elements.append(Spacer(1, 12))

    # List of health data images (3 images)
    health_images = ['/content/descriptive_statistics_table.png', '/content/boxplot_img.png',
                     '/content/piechart.png']

    # Add images to the second section
    for image_path in health_images:
        img = PDFImage(image_path)
        img.drawHeight = 3 * inch  # Set height
        img.drawWidth = 3 * inch  # Set width
        elements.append(img)
        elements.append(Spacer(1, 10))  # Space between images

    # Build the PDF
    doc.build(elements)
    print(f"PDF file created and saved at {filename}")

# Generate PDF
create_pdf(pdf_path)

pip install PyMuPDF

pip install PyPDF2 google-cloud google-generativeai



import google.generativeai as genai
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# Initialize the Google Generative AI model
genai.configure(api_key="AIzaSyDcq55RNDRfWRQ3kRPj8avcb6KaTGVony8")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Define the images you have stored in your content folder
images_folder = '/content'
image_filenames = [
    'kmeanscluster.png',
    'linearstretch.png',
    'hist1.png',
    'hist2.png',
    'hist3.png',
    'descriptive_statistics_table.png',
    'boxplot_img.png',
    'piechart.png'
]

# Prepare a detailed analysis prompt for the Generative AI model
def generate_image_analysis_prompt(images):
    prompt = """The images represent various analyses conducted on a land image where RGB colors are detected.
No specific information about the plant type can be provided.

The following analysis was obtained:
1. K-Means clustering of the RGB image to categorize different areas.
2. Linear stretching of the image to normalize pixel values between 0 and 1.
   The linear stretch was done from 0 to 1, with the following bins considered:
   [0, 0.5, 0.665, 0.83, 1], labeled as:
   ['Dead plant', 'Unhealthy plant', 'Moderately healthy plant', 'Very Healthy plant'].

The images include:
- K-Means clustering results: {0}
- Linear stretch results: {1}
- Histogram 1: {2}
- Histogram 2: {3}
- Histogram 3: {4}
- Descriptive statistics table: {5}
- Boxplot: {6}
- Pie chart: {7}

Please provide an overall analysis and comparison between the plant types based on these images,
focusing on the numerical data present in the statistics and visualizations.
Do not include the image links in the output.
Give the heading as Plant Health Analysis. Give suggestions to the farmers on the basis of
data and give it in simple way. Give everything in Hindi. Remove bold text.""".format(
        os.path.join(images_folder, images[0]),  # K-Means clustering
        os.path.join(images_folder, images[1]),  # Linear stretch
        os.path.join(images_folder, images[2]),  # Histogram 1
        os.path.join(images_folder, images[3]),  # Histogram 2
        os.path.join(images_folder, images[4]),  # Histogram 3
        os.path.join(images_folder, images[5]),  # Descriptive statistics
        os.path.join(images_folder, images[6]),  # Boxplot
        os.path.join(images_folder, images[7])   # Pie chart
    )

    return prompt

# Generate analysis prompt based on existing images
image_analysis_prompt = generate_image_analysis_prompt(image_filenames)

# Provide insights based on the generated prompt
response = model.generate_content(image_analysis_prompt)

# Function to format the response text for PDF
def format_text_for_pdf(output_text):
    formatted_text = []
    lines = output_text.split('\n')

    for line in lines:
        # Clean the line from any unwanted image paths or formatting
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        formatted_text.append(('normal', line))

    return formatted_text

# Function to create a formatted PDF
def create_formatted_pdf(output_text, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)

    # Write the main heading
    main_heading = "Plant Health Analysis"
    c.setFont("Helvetica-Bold", 20)
    text_width = c.stringWidth(main_heading, "Helvetica-Bold", 20)
    c.drawString((width - text_width) / 2, height - 50, main_heading)  # Center the heading

    # Define the maximum width of the text block
    max_text_width = width - 144  # Leave margins on both sides
    y_position = height - 80  # Starting position for the first line

    # Format the response text
    formatted_text = format_text_for_pdf(output_text)

    # Loop through formatted text and add to PDF
    for style, line in formatted_text:
        # Set font based on style
        c.setFont("Helvetica", 12)

        # Split the line into multiple lines to fit the page width
        wrapped_lines = simpleSplit(line.strip(), "Helvetica", 12, max_text_width)

        for wrapped_line in wrapped_lines:
            # Draw the text and adjust position for the next line
            c.drawString(72, y_position, wrapped_line)
            y_position -= 15  # Move down for the next line

            # Create a new page if y_position is too low
            if y_position < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - 50

    # Finalize the PDF document
    c.save()
    print(f"PDF file '{pdf_filename}' created successfully.")

# Create PDF with the formatted analysis response
pdf_filename = '/content/plant_analysis_report_formatted.pdf'
create_formatted_pdf(response.text, pdf_filename)





#LANGUAGES

import google.generativeai as genai
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Initialize the Google Generative AI model
genai.configure(api_key="AIzaSyDcq55RNDRfWRQ3kRPj8avcb6KaTGVony8")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Define the images you have stored in your content folder
images_folder = '/content'
image_filenames = [
    'kmeanscluster.png',
    'linearstretch.png',
    'hist1.png',
    'hist2.png',
    'hist3.png',
    'descriptive_statistics_table.png',
    'boxplot_img.png',
    'piechart.png'
]

# Prepare a detailed analysis prompt for the Generative AI model
def generate_image_analysis_prompt(images, language="Hindi"):
    prompt = """The images represent various analyses conducted on a land image where RGB colors are detected.
No specific information about the plant type can be provided.

The following analysis was obtained:
1. K-Means clustering of the RGB image to categorize different areas.
2. Linear stretching of the image to normalize pixel values between 0 and 1.
   The linear stretch was done from 0 to 1, with the following bins considered:
   [0, 0.5, 0.665, 0.83, 1], labeled as:
   ['Dead plant', 'Unhealthy plant', 'Moderately healthy plant', 'Very Healthy plant'].

The images include:
- K-Means clustering results: {0}
- Linear stretch results: {1}
- Histogram 1: {2}
- Histogram 2: {3}
- Histogram 3: {4}
- Descriptive statistics table: {5}
- Boxplot: {6}
- Pie chart: {7}

Give in simple {language}. Please provide an overall analysis and comparison between the plant types based on these images,
focusing on the numerical data present in the statistics and visualizations.
Do not include the image links in the output.
Give the heading as Plant Health Analysis.
Give suggestions to the farmers on the basis of data and give it in simple way.
Remove bold text.Give in easy readable language.""".format(
        os.path.join(images_folder, images[0]),  # K-Means clustering
        os.path.join(images_folder, images[1]),  # Linear stretch
        os.path.join(images_folder, images[2]),  # Histogram 1
        os.path.join(images_folder, images[3]),  # Histogram 2
        os.path.join(images_folder, images[4]),  # Histogram 3
        os.path.join(images_folder, images[5]),  # Descriptive statistics
        os.path.join(images_folder, images[6]),  # Boxplot
        os.path.join(images_folder, images[7]),  # Pie chart
        language=language  # Add language variable
    )

    return prompt

# Generate analysis prompt based on existing images
image_analysis_prompt = generate_image_analysis_prompt(image_filenames, language)

# Provide insights based on the generated prompt
response = model.generate_content(image_analysis_prompt)

# Function to format the response text for PDF
def format_text_for_pdf(output_text):
    formatted_text = []
    lines = output_text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        formatted_text.append(('normal', line))

    return formatted_text

# Function to check if the text contains Hindi characters
def is_hindi(text):
    # Hindi Unicode range: 0x0900-0x097F
    return any('\u0900' <= char <= '\u097F' for char in text)

# Function to create a formatted PDF
def create_formatted_pdf(output_text, pdf_filename, language):
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Choose the font based on the language of the output
    if is_hindi(output_text) or language.lower() == "hindi":
        pdfmetrics.registerFont(TTFont('NotoSansDevanagari', '/content/NotoSansDevanagari.ttf'))  # Path to your TTF file
        c.setFont("NotoSansDevanagari", 20)  # Use Noto Sans Devanagari for the main heading
        main_font = "NotoSansDevanagari"  # Store font name for later use
    else:
        c.setFont("Helvetica", 20)  # Use Helvetica for the main heading
        main_font = "Helvetica"  # Store font name for later use

    width, height = letter

    # Write the main heading
    main_heading = "Plant Health Analysis"
    text_width = c.stringWidth(main_heading, main_font, 20)  # Use stored font name
    c.drawString((width - text_width) / 2, height - 50, main_heading)  # Center the heading

    # Define the maximum width of the text block
    max_text_width = width - 144  # Leave margins on both sides
    y_position = height - 80  # Starting position for the first line

    # Format the response text
    formatted_text = format_text_for_pdf(output_text)

    # Loop through formatted text and add to PDF
    for style, line in formatted_text:
        if is_hindi(line) or language.lower() == "hindi":
            c.setFont("NotoSansDevanagari", 12)  # Use Noto Sans Devanagari for body text if Hindi
        else:
            c.setFont("Helvetica", 12)  # Use Helvetica for body text if English

        # Split the line into multiple lines to fit the page width
        wrapped_lines = simpleSplit(line.strip(), main_font, 12, max_text_width)  # Use stored font name

        for wrapped_line in wrapped_lines:
            # Draw the text and adjust position for the next line
            c.drawString(72, y_position, wrapped_line)
            y_position -= 15  # Move down for the next line

            # Create a new page if y_position is too low
            if y_position < 50:
                c.showPage()
                if is_hindi(wrapped_line) or language.lower() == "hindi":
                    c.setFont("NotoSansDevanagari", 12)
                else:
                    c.setFont("Helvetica", 12)
                y_position = height - 50

    # Finalize the PDF document
    c.save()
    print(f"PDF file '{pdf_filename}' created successfully.")

# Create PDF with the formatted analysis response
pdf_filename = '/content/plant_analysis_report_formatted.pdf'
create_formatted_pdf(response.text, pdf_filename, language)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging

# Set up logging
logging.basicConfig(filename='email_sending.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# File paths
pdf_path = "/content/plant_analysis_report_formatted.pdf"  # PDF brochure

# Email details
from_address = "sethvanshita@gmail.com"  # Replace with your email address
subject = 'Plant health analysis report and suggestion '

# SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = "sethvanshita@gmail.com"  # Replace with your email address
smtp_password = "hfpr ztwd qaia ohpi"  # Replace with your app password

# Function to send email with PDF attachment
def send_email(email_id, name):
    # Create email body dynamically
    body = f"""
    <p>Hi {name},</p>
    <p>I hope this message finds you well. Attached is the plant health analysis report.</p>
    <p>Yours sincerely,<br>CropSky</p>
    """

    message = MIMEMultipart()
    message['From'] = from_address
    message['To'] = email_id
    message['Subject'] = subject

    message.attach(MIMEText(body, 'html'))

    with open(pdf_path, "rb") as pdf:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(pdf.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={pdf_path}",
        )
        message.attach(part)

    # Send the email with error handling
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = message.as_string()
        server.sendmail(from_address, email_id, text)
        logging.info(f"Email sent successfully to {name} at {email_id}!")
        print(f"Email sent successfully to {name} at {email_id}!")
    except smtplib.SMTPException as e:
        logging.error(f"Error: {e} while sending to {name} at {email_id}")
        print(f"Error: {e} while sending to {name} at {email_id}")
    finally:
        server.quit()


send_email(email_id, name)
