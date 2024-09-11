document.addEventListener('DOMContentLoaded', function() {
    showTab('tab1');
});

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
        if (tabId === "tab2") {
            showLoadWorkflowList(tabId);
        } else if (tabId === "tab1") {
            showGalleryWorkflowList(tabId);
        }
    }
}

function createGridItem(workflowName, container, thumbnail, author = '', time = '') {
    var gridItem = document.createElement('div');
    gridItem.className = 'grid-item';
    gridItem.style.backgroundImage = `url('${thumbnail}')`;
    gridItem.style.backgroundSize = 'cover';
    gridItem.style.backgroundPosition = 'center';
    gridItem.style.backgroundRepeat = 'no-repeat';

    var caption = document.createElement('div');
    caption.className = 'caption';

    var h3 = document.createElement('h3');
    h3.textContent = workflowName;

    var pAuthor = document.createElement('p');
    pAuthor.textContent = `Author: ${author}`;

    var pTime = document.createElement('p');
    pTime.textContent = `Date: ${time}`;

    var link = document.createElement('a');
    link.href = '#';
    link.textContent = 'Load';
    link.onclick = function(e) {
        e.preventDefault();
        sendWorkflow(workflowName);
    };

    var deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = function(e) {
        e.preventDefault();
        deleteWorkflow(workflowName);
    };

    caption.appendChild(h3);
    if (author) caption.appendChild(pAuthor);
    if (time) caption.appendChild(pTime);
    caption.appendChild(link);
    caption.appendChild(deleteButton);

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

                createGridItem(title, container, thumbnail, author, time);
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
                // 提取文件名（去除扩展名）
                const title = workflowName.replace(/\.json$/, '');

                // 生成缩略图
                const thumbnail = generateThumbnailFromContent({ title });

                // 创建并添加网格项
                createGridItem(title, container, thumbnail);
            });
        })
        .catch(error => {
            console.error('Error fetching workflow list:', error);
            alert('Fetch workflow list error.');
        });
}

// 缩略图生成函数
function generateThumbnailFromContent(content) {
    const canvas = document.createElement('canvas');
    canvas.width = 150;
    canvas.height = 150;
    const ctx = canvas.getContext('2d');

    // 设置背景色
    ctx.fillStyle = '#f0f0f0';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 设置字体样式
    ctx.font = 'italic bold 14px "Helvetica Neue", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = '#333';

    // 绘制文本
    ctx.fillText(content.title, canvas.width / 2, canvas.height / 2 + 20);

    return canvas.toDataURL();
}
