document.addEventListener("DOMContentLoaded", function () {

    const categoryField = document.getElementById("id_category");

    if (!categoryField) {
        return;
    }

    const categories = [
        "Director",
        "Professor",
        "Postdoctoral Researcher",
        "PhD Student",
        "Master's Student",
        "Undergraduate Student",
        "Research Assistant",
        "Visiting Scholar",
        "Visiting Student",
        "Alumni",
        "Other"
    ];


    /*
        CREATE DROPDOWN
    */

    const dropdown = document.createElement("div");

    dropdown.id = "team-category-dropdown";


    /*
        IMPORTANT:
        Put the dropdown directly inside BODY.

        This prevents Django Admin form containers
        and the Upload Picture section from covering it.
    */

    document.body.appendChild(dropdown);


    /*
        DROPDOWN STYLE
    */

    dropdown.style.position = "fixed";
    dropdown.style.display = "none";
    dropdown.style.backgroundColor = "#ffffff";
    dropdown.style.border = "1px solid #b8c2cc";
    dropdown.style.borderRadius = "6px";
    dropdown.style.boxShadow = "0 8px 20px rgba(0, 0, 0, 0.20)";
    dropdown.style.zIndex = "2147483647";
    dropdown.style.maxHeight = "280px";
    dropdown.style.overflowY = "auto";
    dropdown.style.overflowX = "hidden";
    dropdown.style.boxSizing = "border-box";


    /*
        POSITION DROPDOWN
    */

    function positionDropdown() {

        const rect =
            categoryField.getBoundingClientRect();


        dropdown.style.left =
            rect.left + "px";


        dropdown.style.top =
            (rect.bottom + 5) + "px";


        dropdown.style.width =
            rect.width + "px";
    }


    /*
        CREATE CATEGORY OPTIONS
    */

    categories.forEach(function (category) {

        const option =
            document.createElement("div");


        option.textContent =
            category;


        option.style.display =
            "block";


        option.style.width =
            "100%";


        option.style.padding =
            "12px 14px";


        option.style.margin =
            "0";


        option.style.cursor =
            "pointer";


        option.style.backgroundColor =
            "#ffffff";


        option.style.color =
            "#26384d";


        option.style.fontSize =
            "14px";


        option.style.fontWeight =
            "400";


        option.style.lineHeight =
            "1.4";


        option.style.textAlign =
            "left";


        option.style.whiteSpace =
            "normal";


        option.style.boxSizing =
            "border-box";


        option.style.borderBottom =
            "1px solid #eeeeee";


        /*
            HOVER
        */

        option.addEventListener(
            "mouseenter",
            function () {

                option.style.backgroundColor =
                    "#eaf2f8";

                option.style.color =
                    "#073f78";

            }
        );


        option.addEventListener(
            "mouseleave",
            function () {

                option.style.backgroundColor =
                    "#ffffff";

                option.style.color =
                    "#26384d";

            }
        );


        /*
            SELECT CATEGORY
        */

        option.addEventListener(
            "mousedown",
            function (event) {

                event.preventDefault();


                categoryField.value =
                    category;


                hideDropdown();


                categoryField.focus();

            }
        );


        dropdown.appendChild(option);

    });


    /*
        SHOW DROPDOWN
    */

    function showDropdown() {

        positionDropdown();

        dropdown.style.display =
            "block";

    }


    /*
        HIDE DROPDOWN
    */

    function hideDropdown() {

        dropdown.style.display =
            "none";

    }


    /*
        CATEGORY FIELD FOCUS
    */

    categoryField.addEventListener(
        "focus",
        function () {

            showDropdown();

        }
    );


    /*
        CATEGORY FIELD CLICK
    */

    categoryField.addEventListener(
        "click",
        function () {

            showDropdown();

        }
    );


    /*
        CATEGORY FIELD TYPING
    */

    categoryField.addEventListener(
        "input",
        function () {

            const typedText =
                categoryField.value
                    .trim()
                    .toLowerCase();


            let visibleCount = 0;


            Array.from(
                dropdown.children
            ).forEach(function (option) {

                const category =
                    option.textContent
                        .toLowerCase();


                if (
                    typedText === "" ||
                    category.includes(typedText)
                ) {

                    option.style.display =
                        "block";

                    visibleCount++;

                } else {

                    option.style.display =
                        "none";

                }

            });


            if (visibleCount > 0) {

                showDropdown();

            } else {

                hideDropdown();

            }

        }
    );


    /*
        CLOSE WHEN CLICKING OUTSIDE
    */

    document.addEventListener(
        "click",
        function (event) {

            if (
                event.target !== categoryField &&
                !dropdown.contains(event.target)
            ) {

                hideDropdown();

            }

        }
    );


    /*
        REPOSITION WHEN SCROLLING
    */

    window.addEventListener(
        "scroll",
        function () {

            if (
                dropdown.style.display !==
                "none"
            ) {

                positionDropdown();

            }

        },
        true
    );


    /*
        REPOSITION WHEN WINDOW RESIZES
    */

    window.addEventListener(
        "resize",
        function () {

            if (
                dropdown.style.display !==
                "none"
            ) {

                positionDropdown();

            }

        }
    );

});