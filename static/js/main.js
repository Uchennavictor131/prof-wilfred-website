document.addEventListener("DOMContentLoaded", function () {

    const mobileButton = document.getElementById("mobileMenuButton");

    const mobileNav = document.getElementById("mobileNav");


    if (mobileButton && mobileNav) {

        mobileButton.addEventListener("click", function () {

            mobileNav.classList.toggle("active");


            const isOpen =
                mobileNav.classList.contains("active");


            mobileButton.setAttribute(
                "aria-expanded",
                isOpen
            );


            const icon =
                mobileButton.querySelector("i");


            if (icon) {

                if (isOpen) {

                    icon.classList.remove("fa-bars");

                    icon.classList.add("fa-xmark");

                } else {

                    icon.classList.remove("fa-xmark");

                    icon.classList.add("fa-bars");

                }

            }

        });

    }


    /* 
       CLOSE MOBILE MENU AFTER CLICKING A LINK
     */

    if (mobileNav) {

        const mobileLinks =
            mobileNav.querySelectorAll("a");


        mobileLinks.forEach(function (link) {

            link.addEventListener("click", function () {

                mobileNav.classList.remove("active");


                if (mobileButton) {

                    mobileButton.setAttribute(
                        "aria-expanded",
                        "false"
                    );


                    const icon =
                        mobileButton.querySelector("i");


                    if (icon) {

                        icon.classList.remove("fa-xmark");

                        icon.classList.add("fa-bars");

                    }

                }

            });

        });

    }

});