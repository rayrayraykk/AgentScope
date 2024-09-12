document.addEventListener('DOMContentLoaded', function() {
    showTab('tab1');
    showGalleryWorkflowList('tab1');
});


function sendWorkflow(fileName) {
    if (confirm('Are you sure you want to import this workflow?')) {
        const workstationUrl = '/workstation?filename=' + encodeURIComponent(fileName);
        window.location.href = workstationUrl;
    }
}

function deleteWorkflow(fileName) {
    if (confirm('Workflow has been deleted？')) {
        fetch('/delete-workflow', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                filename: fileName,
            })
        }).then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                showLoadWorkflowList('tab2');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('delete workflow error.');
        });
    }
}

function showTab(tabId) {
    var tabs = document.getElementsByClassName("tab");
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove("active");
        tabs[i].style.display = "none";
    }
    var tab = document.getElementById(tabId);
    if (tab) {
        tab.classList.add("active");
        tab.style.display = "block";

        var tabButtons = document.getElementsByClassName("tab-button");
        for (var j = 0; j < tabButtons.length; j++) {
            tabButtons[j].classList.remove("active");
        }
        var activeTabButton = document.querySelector(`.tab-button[onclick*="${tabId}"]`);
        if (activeTabButton) {
            activeTabButton.classList.add("active");
        }

        if (tabId === "tab2") {
            showLoadWorkflowList(tabId);
        } else if (tabId === "tab1") {
            showGalleryWorkflowList(tabId);
        }
    }
}


function createGridItem(workflowName, container, thumbnail, author = '', time = '', showDeleteButton = false) {
    var gridItem = document.createElement('div');
    gridItem.className = 'grid-item';

    var img = document.createElement('div');
    img.className = 'thumbnail';
    img.style.backgroundImage = `url('${thumbnail}')`;
    img.style.backgroundSize = 'cover';
    img.style.backgroundPosition = 'center';
    img.style.height = '60%';
    gridItem.appendChild(img);

    var caption = document.createElement('div');
    caption.className = 'caption';
    caption.style.height = '40%';

    var h6 = document.createElement('h6');
    h6.textContent = workflowName;
    h6.style.margin = '3px 0';

    var pAuthor = document.createElement('p');
    pAuthor.textContent = `Author: ${author}`;
    pAuthor.style.margin = '3px 0';
    pAuthor.style.fontSize = '10px';

    var pTime = document.createElement('p');
    pTime.textContent = `Date: ${time}`;
    pTime.style.margin = '3px 0';
    pTime.style.fontSize = '10px';

    var link = document.createElement('a');
    link.href = '#';
    link.textContent = 'Load';
    link.style.marginRight = '5px';
    link.onclick = function(e) {
        e.preventDefault();
        sendWorkflow(workflowName);
    };

    caption.appendChild(h6);
    if (author) caption.appendChild(pAuthor);
    if (time) caption.appendChild(pTime);
    caption.appendChild(link);

    if (showDeleteButton) {
        var deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = function(e) {
            e.preventDefault();
            deleteWorkflow(workflowName);
        };
        caption.appendChild(deleteButton);
    }

    gridItem.appendChild(caption);
    container.appendChild(gridItem);
    console.log('Grid item appended:', gridItem);
}



function showGalleryWorkflowList(tabId) {
    const container = document.getElementById(tabId).querySelector('.grid-container');
    container.innerHTML = '';

    fetch('/fetch-gallery', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched gallery data:', data);

            const workflows = data.json || [];

            if (!Array.isArray(workflows)) {
                console.error('The server did not return an array as expected.', data);
                workflows = [workflows];
            }

            workflows.forEach(workflow => {
                const meta = workflow.meta;
                const title = meta.title;
                const author = meta.author;
                const time = meta.time;
                const thumbnail = meta.thumbnail || generateThumbnailFromContent(meta);
                createGridItem(title, container, thumbnail, author, time, false);
            });
        })
        .catch(error => {
            console.error('Error fetching gallery workflows:', error);

        });
}

function showLoadWorkflowList(tabId) {
    fetch('/list-workflows', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
        .then(response => response.json())
        .then(data => {
            if (!Array.isArray(data.files)) {
                throw new TypeError('The return data is not an array');
            }

            const container = document.getElementById(tabId).querySelector('.grid-container');
            container.innerHTML = '';

            data.files.forEach(workflowName => {
                const title = workflowName.replace(/\.json$/, '');
                const thumbnail = generateThumbnailFromContent({ title });
                createGridItem(title, container, thumbnail, '', '', true);
            });
        })
        .catch(error => {
            console.error('Error fetching workflow list:', error);
            alert('Fetch workflow list error.');
        });
}


function generateThumbnailFromContent(content) {
    const canvas = document.createElement('canvas');
    canvas.width = 150;
    canvas.height = 150;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = '#f0f0f0';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.font = 'italic bold 14px "Helvetica Neue", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = '#333';

    ctx.fillText(content.title, canvas.width / 2, canvas.height / 2 + 20);

    return canvas.toDataURL();
}
