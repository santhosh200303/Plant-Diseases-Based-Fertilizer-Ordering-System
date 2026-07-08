# Plant-Diseases-Based-Fertilizer-Ordering-System
The Plant Diseases Based Fertilizer Ordering System is a web-based application developed to help farmers identify plant diseases at an early stage and purchase suitable fertilizers through an online platform. The system combines Deep Learning with E-Commerce to provide an intelligent and user-friendly solution for modern agriculture.

Users can upload an image of a plant leaf, and the system uses a Convolutional Neural Network (CNN) model built with PyTorch to detect the disease. Based on the prediction, the application displays the disease name, its description, preventive measures, and recommends appropriate fertilizers. Farmers can then browse the available fertilizer products, add them to the cart, and place orders directly through the application.

The system includes separate modules for Admin and Customer. The Admin can manage products, customers, orders, and feedback, while customers can register, log in, detect plant diseases, order fertilizers, track their orders, and download invoices.

#Features

 Plant disease detection using CNN (PyTorch)
 Leaf image upload and automatic disease prediction
 Fertilizer recommendation based on detected disease
 Online fertilizer ordering system
 Customer registration and login
 Shopping cart and order management
 Invoice generation
 Order tracking with delivery status
 Customer feedback module
 Admin dashboard for managing products, customers, orders, and feedback.

 #Technologies
 
Frontend

HTML5,CSS3,Bootstrap,JavaScript
Backend

Python,Flask,Database,MySQL
Machine Learning

PyTorch,TorchVision,CNN (Convolutional Neural Network)
Python Libraries

Flask
Gunicorn
NumPy
Pandas
Pillow
Torch
TorchVision
MySQL Connector Python

#Workflow
User uploads a plant leaf image.
The CNN model analyzes the image.
The system predicts the plant disease.
Disease details and prevention methods are displayed.
Suitable fertilizers are recommended.
Customer adds fertilizers to the cart.
Customer places an order.
Admin processes the order and updates its status.
Customer can track the order and download the invoice.

#Objectives
The main objective of this project is to provide farmers with an intelligent system that can identify plant diseases accurately and recommend suitable fertilizers while also offering a complete online fertilizer purchasing platform. This helps reduce crop loss, improve productivity, and simplify fertilizer procurement.
