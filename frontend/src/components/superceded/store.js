import React, { useState, useEffect } from 'react';
import './App.css';
import html2canvas from 'html2canvas';
import * as XLSX from 'xlsx';

function EmailList() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showTable, setShowTable] = useState(false);
  const [showParsedData, setShowParsedData] = useState({}); // Track visibility of parsed data for each email

  const fetchEmails = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/project-info");
      const data = await response.json();
      console.log(data);
      setEmails(data);
    } catch (error) {
      console.error('Error fetching emails:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (showTable) {
      fetchEmails();
    }
  }, [showTable]);

  // Toggle parsed file data visibility for a specific email
  const toggleParsedDataVisibility = (index) => {
    setShowParsedData(prevState => ({
      ...prevState,
      [index]: !prevState[index], // Toggle the visibility for this email
    }));
  };

  // Function to capture the parsed data section as an image and trigger download
  const downloadParsedDataAsImage = (index) => {
    const element = document.getElementById(`parsed-data-${index}`); // Get the parsed data container by ID
    if (element) {
      html2canvas(element).then((canvas) => {
        const link = document.createElement('a');
        link.href = canvas.toDataURL('image/png'); // Convert canvas to image
        link.download = `parsed-data-${index}.png`; // Set the download file name
        link.click(); // Trigger download
      });
    }
  };

  // Function to export the table to an Excel file
  const exportToExcel = () => {
    const ws = XLSX.utils.json_to_sheet(emails); // Convert emails data to a worksheet
    const wb = XLSX.utils.book_new(); // Create a new workbook
    XLSX.utils.book_append_sheet(wb, ws, 'Emails'); // Append the worksheet to the workbook

    // Create and trigger the download
    XLSX.writeFile(wb, 'emails.xlsx');
  };

  return (
    <div className="emails-section">
      <h1>POExtractor</h1>
      <button onClick={() => setShowTable(!showTable)}>
        {showTable ? 'Hide Emails' : 'Show Emails'}
      </button>

      {loading && showTable && <p>Loading...</p>}

      {showTable && !loading && emails.length > 0 ? (
        <div className="emails-table-container">
          <button onClick={exportToExcel} className="export-excel">
            Export to Excel
          </button>
          <table className="emails-table">
            <thead>
              <tr>
                <th>Subject</th>
                <th>Sender</th>
                <th>Date</th>
                <th>Body</th>
                <th>PO Detected</th>
                <th>Attachments</th>
                <th>Parsed File Data</th>
              </tr>
            </thead>
            <tbody>
              {emails.map((email, index) => (
                <tr key={index}>
                  <td>{email.subject}</td>
                  <td>{email.sender}</td>
                  <td>{email.date}</td>
                  <td>{email.body}</td>
                  <td>{email.po_detected}</td>
                  <td>
                    {email.attachments && email.attachments.length > 0 ? (
                      <ul>
                        {email.attachments.map((attachment, i) => (
                          <li key={i}>{attachment}</li>
                        ))}
                      </ul>
                    ) : (
                      ''
                    )}
                  </td>
                  <td>
                    {email.attachments && email.attachments.length > 0 && (
                      <button onClick={() => toggleParsedDataVisibility(index)}>
                        {showParsedData[index] ? 'Hide Parsed Data' : 'Show Parsed Data'}
                      </button>
                    )}

                    {/* Display parsed file data if the button was clicked */}
                    {showParsedData[index] && email.parsed_files_data && Object.keys(email.parsed_files_data).length > 0 && (
                      <div id={`parsed-data-${index}`}>
                        {Object.keys(email.parsed_files_data).map((fileKey, i) => (
                          <div key={i}>
                            <h6>{fileKey}</h6>
                            <pre>{JSON.stringify(email.parsed_files_data[fileKey], null, 2)}</pre>
                          </div>
                        ))}

                        {/* Button to download parsed data as image */}
                        <button className="download-parsed-data" onClick={() => downloadParsedDataAsImage(index)}>
                          Download Parsed Data as Image
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        showTable && <p>No emails to display</p>
      )}
    </div>
  );
}

export default EmailList;
