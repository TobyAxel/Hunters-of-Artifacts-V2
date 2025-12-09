// Helper function for easier html elements creation
function createElement(type, props) {
    const element = document.createElement(type);

    for (let prop in props) {
        if(prop === "className") {
            props["class"] = props["className"];
            prop = "class";
        }
        element.setAttribute(prop, props[prop]);
    }

    return element;
}
