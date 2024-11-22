class Notification {
  static clearInstances() {
    Notification.count = 0;
    Notification.instances = [];
  }

  constructor(props) {
    Notification.count += 1;
    Notification.instances.push(this);
    this.currentIndex = Notification.count;
    this.position = "bottom-right";
    this.title = "Notification Title";
    this.content = "Notification Content";
    this.element = null;
    this.closeBtn = true;
    this.progress = false;
    this.intervalTime = 3000;
    this.confirmBtn = false;
    this.cancelBtn = false;
    this.pause = true;
    this.reduceNumber = 0;

    // 绑定 this
    this.destroyAll = this.destroyAll.bind(this);
    this.onCancelCallback = this.onCancelCallback.bind(this);
    this.onConfirmCallback = this.onConfirmCallback.bind(this);

    this.init(props);
  }

  init(props) {
    this.setDefaultValues(props);
    this.element = document.createElement("div");
    this.element.className = "notification";
    this.title && this.renderTitle(getCookie("locale") == "zh" ? props.i18nTitle : this.title);
    this.closeBtn && this.renderCloseButton();
    this.content && this.renderContent(getCookie("locale") == "zh" ? props.i18nContent : this.content);
    (this.confirmBtn || this.cancelBtn) && this.renderClickButton();
    this.progress && this.renderProgressBar();
    this.setPosition(this.position);
    document.body.appendChild(this.element);
    setTimeout(() => {
      this.show();
    }, 10);
  }

  isHTMLString(string) {
    const doc = new DOMParser().parseFromString(string, "text/html");
    return Array.from(doc.body.childNodes).some(node => node.nodeType === 1);
  }

  renderCloseButton() {
    this.closeBtn = document.createElement("span");
    this.closeBtn.className = "notification-close";
    this.closeBtn.innerText = "X";
    this.closeBtn.onclick = this.destroyAll;
    this.title.appendChild(this.closeBtn);
  }

  renderTitle(component) {
    if (this.isHTMLString(component)) {
      this.title = document.createElement("div");
      this.title.className = "notification-title";
      this.title.innerHTML = component;
    } else {
      this.title = document.createElement("div");
      this.titleText = document.createElement("div");
      this.title.className = "notification-title";
      this.titleText.className = "notification-titleText";
      this.titleText.innerText = component;
      this.title.appendChild(this.titleText);
    }
    this.element.appendChild(this.title);
  }

  renderContent(component) {
    if (this.isHTMLString(component)) {
      this.content = document.createElement("div");
      this.content.className = "notification-content";
      this.content.innerHTML = component;
    } else {
      this.content = document.createElement("div");
      this.content.className = "notification-content";
      this.content.innerText = component;
    }
    this.element.appendChild(this.content);
  }

  renderClickButton() {
    if (this.confirmBtn || this.cancelBtn) {
      this.clickBottonBox = document.createElement("div");
      this.clickBottonBox.className = "notification-clickBotton-box";
    }
    if (this.confirmBtn) {
      this.confirmBotton = document.createElement("button");
      this.confirmBotton.className = "notification-btn confirmBotton";
      this.confirmBotton.innerText = getCookie("locale") == "zh" ? this.i18nConfirmBtn : this.confirmBtn;
      this.confirmBotton.onclick = this.onConfirmCallback;
      this.clickBottonBox.appendChild(this.confirmBotton);
    }
    if (this.cancelBtn) {
      this.cancelBotton = document.createElement("button");
      this.cancelBotton.className = "notification-btn cancelBotton";
      this.cancelBotton.innerText = getCookie("locale") == "zh" ? this.i18nCancelBtn : this.cancelBtn;
      this.cancelBotton.onclick = this.onCancelCallback;
      this.clickBottonBox.appendChild(this.cancelBotton);
    }
    this.element.appendChild(this.clickBottonBox);
  }

  renderProgressBar() {
    this.progressBar = document.createElement("div");
    this.progressBar.className = "notification-progress";
    this.element.appendChild(this.progressBar);
  }

  stepProgressBar(callback) {
    const startTime = performance.now();
    const step = (timestamp) => {
      const progress = Math.min((timestamp + this.reduceNumber - startTime) / this.intervalTime, 1);
      this.progressBar.style.width = (1 - progress) * 100 + "%";
      if (progress < 1 && this.pause === false) {
        requestAnimationFrame(step);
      } else {
        this.reduceNumber = timestamp + this.reduceNumber - startTime;
      }
      if (progress === 1) {
        this.pause = true;
        this.reduceNumber = 0;
        callback();
        this.removeChild();
      }
    };
    requestAnimationFrame(step);
  }

  setDefaultValues(props) {
    for (const key in props) {
      if (props[key] !== undefined) {
        this[key] = props[key];
      }
    }
  }

  setPosition() {
    switch (this.position) {
    case "top-left":
      this.element.style.top = "25px";
      this.element.style.left = "-100%";
      break;
    case "top-right":
      this.element.style.top = "25px";
      this.element.style.right = "-100%";
      break;
    case "bottom-right":
      this.element.style.bottom = "25px";
      this.element.style.right = "-100%";
      break;
    case "bottom-left":
      this.element.style.bottom = "25px";
      this.element.style.left = "-100%";
      break;
    }
  }

  show() {
    this.element.style.display = "flex";
    switch (this.position) {
    case "top-left":
      this.element.style.top = "25px";
      this.element.style.left = "25px";
      break;
    case "top-right":
      this.element.style.top = "25px";
      this.element.style.right = "25px";
      break;
    case "bottom-right":
      this.element.style.bottom = "25px";
      this.element.style.right = "25px";
      break;
    case "bottom-left":
      this.element.style.bottom = "25px";
      this.element.style.left = "25px";
      break;
    }
  }

  destroyAll() {
    for (const instance of Notification.instances) {
      document.body.removeChild(instance.element);
    }
    Notification.clearInstances();
  }

  removeChild() {
    let removeIndex;
    for (let i = 0; i < Notification.instances.length; i++) {
      if (Notification.instances[i].currentIndex === this.currentIndex) {
        removeIndex = i;
        break;
      }
    }
    if (removeIndex !== undefined) {
      Notification.instances.splice(removeIndex, 1);
    }
    this.element.remove();
  }

  addCloseListener() {
    this.closeBtn.addEventListener("click", () => {
      this.removeChild();
    });
  }

  onCancelCallback() {
    if (typeof this.onCancel === "function") {
      this.onCancel();
      this.removeChild();
    }
  }

  onConfirmCallback() {
    if (typeof this.onConfirm === "function") {
      this.pause = !this.pause;
      if (!this.pause) {
        this.stepProgressBar(this.onConfirm);
        this.confirmBotton.innerText = getCookie("locale") === "zh" ? "暂停" : "pause";
      } else {
        this.confirmBotton.innerText = this.confirmBtn;
      }
    }
  }
}

Notification.count = 0;
Notification.instances = [];

class KVPairs extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.kvname = "";
    this.lang = getCookie("locale") || "en";
    this.initUI();
  }

  initUI() {
    const container = document.createElement("div");
    container.className = "kv-container";
    this.kvname = this.getAttribute("kv-name");

    const addBtnHTML = `
            <button id="add-btn">${this.lang == "en" ? "Add" : "添加"}</button>
        `;

    this.shadowRoot.appendChild(container);
    this.shadowRoot.innerHTML += addBtnHTML;

    const addBtn = this.shadowRoot.querySelector("#add-btn");
    addBtn.addEventListener("click", () => this.addKVPair());

    const style = document.createElement("style");
    style.textContent = `
            .kv-container {
                margin-bottom: 20px;
            }

            .kv-pair {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
                gap:10px
            }

            .kv-pair input {
                flex: 1; /* 使输入框自适应宽度 */
                height: 32px;
                padding: 4px 11px;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                font-size: 14px;
                line-height: 1.5;
                color: rgba(0, 0, 0, 0.65);
                background-color: #fff;
                transition: all 0.3s;
            }

            .kv-pair input:focus {
                border-color: #1890ff;
                box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
                outline: none;
            }

            .kv-pair button.remove-btn {
                padding: 0 15px;
                height: 32px;
                border: 1px solid #ff4d4f;
                border-radius: 4px;
                background-color: #ff4d4f;
                color: #fff;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.3s;
                box-sizing: content-box;
                display:none;
            }

            .kv-pair button.remove-btn:hover {
                border-color: #ff7875;
                background-color: #ff7875;
            }

            .kv-pair button.remove-btn:active {
                background-color: #fa541c;
            }

            button#add-btn {
                width: 100%; /* 占满一行 */
                padding: 0 15px;
                height: 32px;
                border: 1px solid #A0D9C4;
                border-radius: 4px;
                background-color: #59AC80;
                color: #fff;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.3s;
            }

            button#add-btn:hover {
                background-color: #3D7D5A;
            }

            button#add-btn:active {
                background-color: #3D7D5A;
            }
        `;

    this.shadowRoot.appendChild(style);
    this.shadowRoot.appendChild(container);
    this.shadowRoot.appendChild(addBtn);

    this.addKVPair();
  }


  addKVPair(key = "", value = "") {

    const container = this.shadowRoot.querySelector(".kv-container");
    const kvPair = document.createElement("div");
    kvPair.innerHTML = `
            <div class="kv-pair">
                <input type="text" placeholder="key" i18n="custom-kvpair-key"  i18n-only="placeholder" k-name=k-${this.kvname}>
                <input type="text" placeholder="value" i18n="custom-kvpair-value"  i18n-only="placeholder" v-name=v-${this.kvname}>
                <button class="remove-btn" i18n="custom-kvpair-button">delete</button>
            </div>
        `;
    container.appendChild(kvPair);
    kvPair.querySelector("input[k-name=\"k-" + this.kvname + "\"]").value = key;
    kvPair.querySelector("input[v-name=\"v-" + this.kvname + "\"]").value =value ;
    const removeBtns = container.querySelectorAll(".remove-btn");
    removeBtns.forEach(btn => {
      btn.addEventListener("click", (event) => {
        event.target.parentElement.remove();

        const remainingPairs = container.querySelectorAll(".kv-pair");
        if (remainingPairs.length === 1) {
          remainingPairs[0].querySelector(".remove-btn").style.display = "none";
        }
        this.dispatchEvent(new CustomEvent("button-clicked", {
          detail: "delete",
          bubbles: true,
          composed: true
        }));
      });
    });

    if (container.childElementCount > 1) {
      container.querySelectorAll(".remove-btn").forEach(btn => {
        btn.style.display = "inline-block";
      });
    }
  }

  getValues() {
    const pairs = [];
    const kvPairs = this.shadowRoot.querySelectorAll(".kv-pair");
    kvPairs.forEach(pair => {
      const key = pair.querySelector("input[k-name=\"k-" + this.kvname + "\"]").value;
      const value = pair.querySelector("input[v-name=\"v-" + this.kvname + "\"]").value;
      if (key && value) {
        pairs.push({ key, value });
      }
    });
    return pairs;
  }

  setData(data) {
    const container = this.shadowRoot.querySelector(".kv-container");
    container.innerHTML = "";

    data.forEach((item) => {
      this.addKVPair(item.key, item.value);
    });
  }
}

customElements.define("kv-pair", KVPairs);

class InfoBubble extends HTMLElement {
  constructor() {
    super();
    const shadow = this.attachShadow({ mode: "open" });
    const url = this.getAttribute("url");
    const template = `
            <style>
                .inner {
                    border-radius: 10px;
                    clip-path: circle(5% at 4% 12px);
                    transition: .5s cubic-bezier(0, 1, 0.6, 1);
                    position: absolute;
                    background-color: gray;
                    margin: 4px 0 0 4px;
                }
                .inner span {
                    float: left;
                    font-weight: 500;
                    font-size: 16px;
                    margin-left: 2%;
                    opacity: 1;
                    color: #fff;
                    transition: opacity 1s;
                }
                .inner p {
                    font-size: 0.8em;
                    visibility: hidden;
                    transition: .5s cubic-bezier(0, 1.44, 0.51, 1.33);
                    margin:10px;
                }
                .inner:hover {
                    clip-path: circle(75%);
                    background-color: #A0D9C4;
                    color: #000;
                }
                .inner:hover p {
                    visibility: visible;
                }
                .inner:hover span {
                    opacity: 0;
                    transition-duration: 0s;
                }
                .inner a {
                  color: blue;
                  cursor: pointer;
                }
            </style>
        `;
    const textblade = getCookie("locale") == "zh" ? `
      <div class="inner">
        <span>?</span>
        <p>访问 <a href=${url} target="_blank">${url}</a> 获取API Key并开通相应模型/服务。</p>
      </div>`
      :
      ` <div class="inner">
          <span>?</span>
          <p>Visit <a href=${url} target="_blank">${url}</a> to get an API key and activate the corresponding model/service.</p>
        </div>`;
    shadow.innerHTML = template + textblade;
  }
}

customElements.define("info-bubble", InfoBubble);