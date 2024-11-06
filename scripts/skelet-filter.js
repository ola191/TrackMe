let data = [];

function applyFilterLogic() {
    const containers = document.querySelectorAll('[data-skelet-filter-container]');

    containers.forEach(container => {
        const containerValue = container.getAttribute('data-skelet-filter-container');
        if (containerValue) {
            data.push({ container: containerValue, filters: {} });
        }

        const draggableItems = container.querySelectorAll('[data-skelet-filter-drag]');

        draggableItems.forEach(item => {
            item.draggable = true;

            item.addEventListener('dragstart', (event) => {
                event.dataTransfer.setData('text', JSON.stringify({
                    dragValue: item.getAttribute('data-skelet-filter-drag'),
                    text: item.textContent,
                    container: containerValue
                }));
            });
        });
    });

    const filterBars = document.querySelectorAll('[data-skelet-filter-bar]');

    filterBars.forEach(bar => {
        bar.addEventListener('dragover', (event) => {
            event.preventDefault();
        });

        bar.addEventListener('drop', (event) => {
            event.preventDefault();

            const draggedData = JSON.parse(event.dataTransfer.getData('text'));
            const { dragValue, text, container } = draggedData;

            let containerData = data.find(d => d.container === container);
            if (!containerData.filters[dragValue]) {
                const newFilter = document.createElement('div');
                newFilter.setAttribute('data-filter-name', dragValue);

                const label = document.createElement('span');
                label.textContent = `${dragValue}: `;

                const input = document.createElement('input');
                input.type = 'text';
                input.value = text;
                input.setAttribute('list', `${dragValue}-options`);
                input.addEventListener('input', () => {
                    containerData.filters[dragValue] = input.value;
                    applyFilters();
                });

                const removeButton = document.createElement('button');
                removeButton.textContent = 'x';
                removeButton.addEventListener('click', () => {
                    delete containerData.filters[dragValue];
                    newFilter.remove();
                    applyFilters();
                });

                const dataList = document.createElement('datalist');
                dataList.id = `${dragValue}-options`;

                const uniqueValues = new Set();
                document.querySelectorAll(`[data-skelet-filter-container="${container}"] [data-skelet-filter-row] [data-skelet-filter-drag="${dragValue}"]`)
                    .forEach(el => uniqueValues.add(el.textContent.trim()));

                uniqueValues.forEach(value => {
                    const option = document.createElement('option');
                    option.value = value;
                    dataList.appendChild(option);
                });

                newFilter.appendChild(label);
                newFilter.appendChild(input);
                newFilter.appendChild(dataList);
                newFilter.appendChild(removeButton);
                bar.appendChild(newFilter);

                containerData.filters[dragValue] = text;
                applyFilters();
            } else {
                const existingInput = bar.querySelector(`[data-filter-name="${dragValue}"] input`);
                if (existingInput) existingInput.value = text;
                containerData.filters[dragValue] = text;
                applyFilters();
            }
        });
    });

    console.log("Collected data:", data);
}

function applyFilters() {
    data.forEach(({ container, filters }) => {
        const containerElement = document.querySelector(`[data-skelet-filter-container="${container}"]`);
        const rows = containerElement.querySelectorAll('[data-skelet-filter-row]');

        rows.forEach(row => {
            let isVisible = true;

            Object.keys(filters).forEach(filter => {
                const matchingElements = row.querySelectorAll(`[data-skelet-filter-drag="${filter}"]`);
                const matchesFilter = Array.from(matchingElements).some(el => el.textContent === filters[filter]);

                if (filters[filter] && !matchesFilter) {
                    isVisible = false;
                }
            });

            row.style.display = isVisible ? '' : 'none';
        });
    });
}

document.addEventListener("DOMContentLoaded", applyFilterLogic);