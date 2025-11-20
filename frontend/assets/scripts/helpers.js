function createElement(type, props) {
    const element = document.createElement(type);

    for (const prop in props) {
        if(prop === "className") prop = "class";
        element.setAttribute(prop, props[prop]);
    }

    return element;
}
