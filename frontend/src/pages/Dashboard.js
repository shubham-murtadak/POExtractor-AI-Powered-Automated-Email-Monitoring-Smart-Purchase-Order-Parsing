import React, { useState } from "react";
import html2canvas from "html2canvas";
import * as XLSX from "xlsx";

function EmailList() {
  const [showParsedData, setShowParsedData] = useState({});

  // Hardcoded Email Data
  const emails = [
    {
      subject: "Purchase Order Confirmation",
      sender: "supplier@example.com",
      date: "2024-02-20",
      body: "Please find attached the purchase order details.",
      po_detected: "Yes",
      attachments: ["PO_12345.pdf"],
      parsed_files_data: {
        "PO_12345.pdf": {
          order_number: "12345",
          amount: "$10,000",
          items: ["Laptop", "Mouse", "Keyboard"]
        }
      }
    },
    {
      subject: "Invoice for Order 67890",
      sender: "billing@company.com",
      date: "2024-02-19",
      body: "Attached is the invoice for your recent order.",
      po_detected: "No",
      attachments: ["Invoice_67890.pdf"],
      parsed_files_data: {
        "Invoice_67890.pdf": {
          invoice_number: "67890",
          amount: "$5,000",
          status: "Paid"
        }
      }
    }
  ];

  const toggleParsedDataVisibility = (index) => {
    setShowParsedData((prevState) => ({
      ...prevState,
      [index]: !prevState[index],
    }));
  };

  const downloadParsedDataAsImage = (index) => {
    const element = document.getElementById(`parsed-data-${index}`);
    if (element) {
      html2canvas(element).then((canvas) => {
        const link = document.createElement("a");
        link.href = canvas.toDataURL("image/png");
        link.download = `parsed-data-${index}.png`;
        link.click();
      });
    }
  };

  const exportToExcel = () => {
    const ws = XLSX.utils.json_to_sheet(emails);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Emails");
    XLSX.writeFile(wb, "emails.xlsx");
  };

  return (
    <div className="emails-section bg-gray-900 text-white min-h-screen p-10">
      {/* Header Section with Title and Buttons */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-4xl font-bold">📩 POExtractor</h1>
        
        <div className="flex gap-4">
          {/* Settings Icon */}

          {/* Export to Excel Button */}
          <button
            onClick={exportToExcel}
            className="bg-green-500 hover:bg-green-500 text-white px-3 py-3 rounded-lg 
                     transition-transform transform hover:scale-105 shadow-lg"
          >
            📊 Export to Excel
          </button>
          <button className="bg-gray-700 hover:bg-gray-800 text-white p-3 rounded-full shadow-lg">
            ⚙️
          </button>
        </div>
      </div>

      {/* Emails Table */}
      <div className="emails-table-container mt-8">
        <div className="overflow-x-auto">
          <table className="w-full border-collapse shadow-lg bg-white/10 backdrop-blur-md border border-white/20 rounded-lg">
            <thead>
              <tr className="bg-blue-600 text-white">
                <th className="p-4">Subject</th>
                <th className="p-4">Sender</th>
                <th className="p-4">Date</th>
                <th className="p-4">Body</th>
                <th className="p-4">PO Detected</th>
                <th className="p-4">Attachments</th>
                <th className="p-4">Parsed File Data</th>
              </tr>
            </thead>
            <tbody>
              {emails.map((email, index) => (
                <tr key={index} className="text-center transition-all hover:bg-blue-500/20">
                  <td className="p-4 border border-white/20">{email.subject}</td>
                  <td className="p-4 border border-white/20">{email.sender}</td>
                  <td className="p-4 border border-white/20">{email.date}</td>
                  <td className="p-4 border border-white/20">{email.body}</td>
                  <td className="p-4 border border-white/20">{email.po_detected}</td>
                  <td className="p-4 border border-white/20">
                    {email.attachments?.length > 0 ? (
                      <ul>
                        {email.attachments.map((attachment, i) => (
                          <li key={i}>{attachment}</li>
                        ))}
                      </ul>
                    ) : (
                      "No Attachments"
                    )}
                  </td>
                  <td className="p-4 border border-white/20">
                    {email.attachments?.length > 0 && (
                      <button
                        onClick={() => toggleParsedDataVisibility(index)}
                        className="bg-purple-600 hover:bg-purple-700 text-white px-3 py-2 rounded-lg 
                                   transition-transform transform hover:scale-105 shadow-md"
                      >
                        {showParsedData[index] ? "Hide Parsed Data" : "Show Parsed Data"}
                      </button>
                    )}

                    {showParsedData[index] &&
                      email.parsed_files_data &&
                      Object.keys(email.parsed_files_data).length > 0 && (
                        <div id={`parsed-data-${index}`} className="mt-3 bg-gray-800 p-4 rounded-md shadow-md">
                          {Object.keys(email.parsed_files_data).map((fileKey, i) => (
                            <div key={i} className="mb-4">
                              <h6 className="text-blue-400 font-bold mb-2">{fileKey}</h6>
                              <table className="w-full border-collapse shadow-md bg-white/10 backdrop-blur-md border border-white/20 rounded-lg">
                                <thead>
                                  <tr className="bg-gray-700 text-white">
                                    <th className="p-3 border border-white/20">Field</th>
                                    <th className="p-3 border border-white/20">Value</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {Object.entries(email.parsed_files_data[fileKey]).map(([key, value], j) => (
                                    <tr key={j} className="text-center transition-all hover:bg-gray-700/20">
                                      <td className="p-3 border border-white/20 capitalize">{key.replace(/_/g, " ")}</td>
                                      <td className="p-3 border border-white/20">
                                        {Array.isArray(value) ? value.join(", ") : value}
                                      </td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>
                          ))}

                          <button
                            onClick={() => downloadParsedDataAsImage(index)}
                            className="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded-lg 
                   transition-transform transform hover:scale-105 shadow-md mt-2"
                          >
                            📷 Download as Image
                          </button>
                        </div>
                      )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default EmailList;
