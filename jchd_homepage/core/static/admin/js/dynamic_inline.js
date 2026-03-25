// static/admin/js/dynamic_inline.js
document.addEventListener("DOMContentLoaded", function () {
    const pageTypeSelect = document.querySelector("#id_page_type");
    if (!pageTypeSelect) return;

    const inlineGroups = document.querySelectorAll(".inline-group");

    function toggleInlines() {
        const selectedType = pageTypeSelect.value;

        inlineGroups.forEach((group) => {
            const groupId = group.id;
            if (groupId.includes("basic_contents") && selectedType === "basic_content") {
                group.style.display = "block";
            } else if (groupId.includes("company_profiles") && selectedType === "company_profile") {
                group.style.display = "block";
            } else if (groupId.includes("history_events") && selectedType === "history") {
                group.style.display = "block";
            } else if (groupId.includes("greetings") && selectedType === "greeting") {
                group.style.display = "block";
            } else if (groupId.includes("global_networks") && selectedType === "global_network") {
                group.style.display = "block";
            } else {
                group.style.display = "none";
            }
        });
    }

    toggleInlines();

    pageTypeSelect.addEventListener("change", toggleInlines);
});
