const nodemailer = require('nodemailer');

const sendEmail = (subject, text) => {
    // Erstelle einen Transporter für Nodemailer
    const transporter = nodemailer.createTransport({
        service: 'Outlook365', // Specify Outlook service
        auth: {
            user: 'Fabian.Stettler_Log@outlook.com',
            pass: 'YR,LCkJ7z9f?P(x'
        }
    });

    const mailOptions = {
        from: 'Fabian.Stettler_Log@outlook.com',
        to: 'fabian.stettler@hispeed.ch',
        subject: subject,
        text: text
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.error(`Error sending email: ${error}`);
        } else {
            console.log(`Email sent: ${info.response}`);
        }
    });
};

module.exports = sendEmail;
