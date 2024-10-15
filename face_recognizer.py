import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
import cv2
from PIL import Image, ImageTk
from datetime import datetime
from rekognition import update_image, check_face

# Function to start the webcam for the "Check User" window
def open_check_user_camera():
    global cap, check_user_window, img_label

    # Create a new window for the camera
    check_user_window = tk.Toplevel(root)
    check_user_window.title("Camera - Check Face")
    check_user_window.geometry("700x550")

    # Create label for displaying video stream
    img_label = ttk.Label(check_user_window)
    img_label.grid(row=0, column=0, columnspan=2)

    # Capture button
    capture_button = ttk.Button(check_user_window, text="Check Face", command=capture_check_user_image)
    capture_button.grid(row=1, column=0, padx=5, pady=10)

    # Quit button to close the camera window
    close_button = ttk.Button(check_user_window, text="Close Camera", command=close_check_user_camera)
    close_button.grid(row=1, column=1, padx=5, pady=10)

    # Start capturing from webcam
    cap = cv2.VideoCapture(0)
    show_check_user_frame()

# Function to show the frames in the Tkinter window
def show_check_user_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip the frame for a mirror effect

    # Resize the frame to fit the window (700x500)
    frame = cv2.resize(frame, (700, 500))

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    img_label.imgtk = imgtk
    img_label.configure(image=imgtk)
    img_label.after(10, show_check_user_frame)

# Function to capture the image from the webcam for "Check User"
def capture_check_user_image():
    # Get current timestamp and format it
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a unique filename using the timestamp
    file_name = f"check_user_{timestamp}.png"

    # Capture the image and save it
    _, frame = cap.read()
    cv2.imwrite(file_name, frame)
    print(f"Image captured and saved as '{file_name}'")
    
    result, confidence = check_face(file_name)
    if result:
        messagebox.showinfo("Info", f"Person recognized: {result} with confidence {confidence}%")
    else:
        messagebox.showinfo("Info", "Person not recognized")

# Function to close the "Check User" camera window
def close_check_user_camera():
    cap.release()
    check_user_window.destroy()
    
# Function to start the webcam and show it in a new window
def open_camera():
    global cap, camera_window, img_label, name_entry

    # Create a new window for the camera
    camera_window = tk.Toplevel(root)
    camera_window.title("Camera - Add Face")
    camera_window.geometry("700x550")

    # Create label for displaying video stream
    img_label = ttk.Label(camera_window)
    img_label.grid(row=0, column=0, columnspan=4)

    # Name entry field label and input box
    name_label = ttk.Label(camera_window, text="Enter Name: ")
    name_label.grid(row=1, column=0, padx=5, pady=10, sticky=tk.E)
    
    name_entry = ttk.Entry(camera_window, width=20)
    name_entry.grid(row=1, column=1, padx=5, pady=10, sticky=tk.W)

    
    # Capture button
    capture_button = ttk.Button(camera_window, text="Capture Image", command=capture_image)
    capture_button.grid(row=1, column=2, pady=10)

    # Quit button to close the camera window
    close_button = ttk.Button(camera_window, text="Close Camera", command=close_camera)
    close_button.grid(row=1, column=3, pady=10)

    # Start capturing from webcam
    cap = cv2.VideoCapture(0)
    show_frame()

# Function to show the frames in the Tkinter window
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip the frame for a mirror effect
     # Resize the frame to fit the window (700x550)
    frame = cv2.resize(frame, (700, 500))

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    img_label.imgtk = imgtk
    img_label.configure(image=imgtk)
    img_label.after(10, show_frame)

# Function to capture the image from the webcam
def capture_image():
    user_name = name_entry.get().strip()
    if not user_name:
        messagebox.showerror("Error", "Please enter a name before capturing the image.")
        return
    
    # Get current timestamp and format it
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Combine user name and timestamp to create a unique filename
    file_name = f"{user_name}_{timestamp}.png"

    # Capture the image and save it
    _, frame = cap.read()
    cv2.imwrite(file_name, frame)
    print(f"Image captured and saved as '{file_name}'")
    
    update_image(user_name, file_name)

# Function to close the camera window
def close_camera():
    cap.release()
    camera_window.destroy()
    
# Create the main window
root = tk.Tk()
root.title("Face Recognizer")
root.geometry("700x500")

# Set the main frame
frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Title Label
title_label = ttk.Label(frame, text="Home Page", font=("Arial", 20))
title_label.grid(row=0, column=0, padx=100, pady=40)

# Buttons
add_user_button = ttk.Button(frame, text="Add Face", width=20, command=open_camera)
add_user_button.grid(row=1, column=0, padx=100, pady=10)

check_user_button = ttk.Button(frame, text="Check Face", width=20, command=open_check_user_camera)
check_user_button.grid(row=2, column=0, padx=100, pady=10)

quit_button = ttk.Button(frame, text="Quit", command=root.quit, width=20)
quit_button.grid(row=3, column=0, padx=100, pady=20)

# Add an image placeholder (currently no actual image loading functionality)
# Load the image 
image = PhotoImage(file="icon.png")
# Create a label to display the image
image_label = tk.Label(root, image=image)
image_label.grid(row=0, column=2, padx=0, pady=80)


# Start the main loop
root.mainloop()
