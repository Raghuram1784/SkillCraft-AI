// sendEmail.js
const express = require("express");
const nodemailer = require("nodemailer");
require("dotenv").config(); // Load environment variables

const app = express();
app.use(express.json());

const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
        user: process.env.EMAIL_USER, // Use environment variable
        pass: process.env.EMAIL_PASS,   // Use environment variable
    },
});

app.post("/send-email", async (req, res) => {
    const { name, email } = req.body;
    const mailOptions = {
        from: process.env.EMAIL_USER, // Use environment variable
        to: "aiskillcraft@gmail.com",   // Admin email
        subject: "New User Registration",
        text: `New user registered:\nName: ${name}\nEmail: ${email}`,
    };

    try {
        await transporter.sendMail(mailOptions);
        res.status(200).send("Email sent successfully!");
    } catch (error) {
        console.error(error);
        res.status(500).send("Failed to send email.");
    }
});

const PORT = 3001;
app.listen(PORT, () => console.log(`Email service running on port ${PORT}`));