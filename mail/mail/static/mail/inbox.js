document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#detail-email-view").style.display = "none";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";

  // Add event listener for the send button
  document.querySelector("#compose-send").addEventListener("click", function () {
    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;
    fetch("http://127.0.0.1:8000/emails", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    }).then((response) => response.json()).then((data) => console.log(data));
  });
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#detail-email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`http://127.0.0.1:8000/emails/${mailbox}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      data.forEach(element => {
        const emailElement = document.createElement("div");
        emailElement.className = "email-item";
        emailElement.style.padding = "5px";
        emailElement.style.border = element.read ? "1px solid #000000" : "1px solid #0000ff";
        emailElement.style.display = "flex";
        emailElement.style.justifyContent = "space-between";
        emailElement.innerHTML = `
          <div><strong>${element.sender}</strong>  ${element.subject}</div>
          <div>${element.timestamp}</div>
          `;
        emailElement.addEventListener("click", () => {
          load_detail(element.id)
        })
        document.querySelector("#emails-view").appendChild(emailElement);

      });
    });
}

function load_detail(email_id) {
  // Show the mailbox and hide other views
  document.querySelector("#detail-email-view").style.display = "block";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  fetch(`http://127.0.0.1:8000/emails/${email_id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      read: true
    })
  })

  fetch(`http://127.0.0.1:8000/emails/${email_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => response.json())
    .then((data) => {
        console.log(data)
        const emailElement = document.createElement("div");
        emailElement.className = "email-item";
        emailElement.innerHTML = `
          <div>
            <strong>From:</strong> ${data.sender} <br \>
            <strong>To:</strong>  ${data.recipients.join(", ")} <br \>
            <strong>Title:</strong> ${data.subject} <br \>
            <strong>Timestamp: </strong> ${data.timestamp}
          </div>
          <button id="reply-button" class="btn btn-sm btn-outline-primary">Reply</button>
          <hr \>
          <div>
            ${data.body}
          </div>
        `;
        document.querySelector("#detail-email-view").replaceChild(emailElement, document.querySelector("#detail-email-view").firstChild);
        document.querySelector("#reply-button").addEventListener("click", () => {
          compose_email();
          document.querySelector("#compose-recipients").value = data.sender;
          if (data.subject.startsWith("Re: ")) {
            document.querySelector("#compose-subject").value = data.subject;
          } else {
            document.querySelector("#compose-subject").value = `Re: ${data.subject}`;
          }
          document.querySelector("#compose-body").value = `On ${data.timestamp} ${data.sender} wrote: \n${data.body}`
        })
    });
}