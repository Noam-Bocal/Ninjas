const express = require('express');
const app = express();
const port = 3000;
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');

app.use(cors()); // Enable CORS for all routes


// Create a new SQLite database connection
const db = new sqlite3.Database('C:\\Users\\user\\Desktop\\נועם לימודים\\rephael\\ninjas\\sql database handle\\attacks_data.db'); 


app.get('/search', (req, res) => {
    const query = req.query.q;
  
    db.all(`SELECT * FROM attacks WHERE Description LIKE '%${query}%'`, (err, rows) => {
      if (err) {
        console.error(err);
        res.status(500).send('An error occurred while searching');
      } else {
        res.json(rows);
      }
    });
  });
  

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
