const PALETTES = {
    tasks: {
        "completed": {backgroundColor: "rgb(100,200,100)"},
        "in progress": {backgroundColor: "rgb(250, 220, 100)"},
        "to do": {backgroundColor: "rgb(250,160,70)"},
    },
    projects: {
        "completed": {backgroundColor: "rgb(100,200,100)"},
        "in progress": {backgroundColor: "rgb(250, 220, 100)"},
        "to do": {backgroundColor: "rgb(250,160,70)"},
    },
    notifications: {
        "accepted": {backgroundColor: "rgb(100,200,100)"},
        "requested" : {backgroundColor: "rgb(250, 220, 100)"},
        "declined": {backgroundColor: "rgb(200, 100, 100)"},
        "blocked": {backgroundColor: "rgb(50, 50, 50)", color: "white"},
    }
};

function applyPaletteStyles() {
    let elements = document.querySelectorAll("[data-palet]");

    elements.forEach(element => {
        let paletteName = element.getAttribute("data-palet");
        let type = element.getAttribute("data-palet-type").toLowerCase();

        if (PALETTES[paletteName] && PALETTES[paletteName][type]) {
            const styles = PALETTES[paletteName][type];
            Object.assign(element.style, styles);
        }
    });
}

document.addEventListener("DOMContentLoaded", applyPaletteStyles);