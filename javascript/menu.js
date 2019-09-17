
//updated ver
* {
  box-sizing:border-box;
}
@import url(https://fonts.googleapis.com/css?family=Lato:400,700);
body {

  font-family:'Lato';
}
.heading-primary {
  font-size:2em;
  padding:2em;
  text-align:center;
}
.accordion dl,
.accordion-list {
   border:1px solid #ddd;
   &:after {
       content: "";
       display:block;
       height:1em;
       width:100%;
       background-color:darken(#38cc70, 10%);
     }
}
.accordion dd,
.accordion__panel {
   background-color:#eee;
   font-size:1em;
   line-height:1.5em;
}
.accordion p {
  padding:1em 2em 1em 2em;
}

.accordion {
    position:relative;
    background-color:#eee;
}
.container {
  max-width:960px;
  margin:0 auto;
  padding:2em 0 2em 0;
}
.accordionTitle,
.accordion__Heading {
 background-color:#38cc70;
   text-align:center;
     font-weight:700;
          padding:2em;
          display:block;
          text-decoration:none;
          color:#fff;
          transition:background-color 0.5s ease-in-out;
  border-bottom:1px solid darken(#38cc70, 5%);
  &:before {
   content: "+";
   font-size:1.5em;
   line-height:0.5em;
   float:left;
   transition: transform 0.3s ease-in-out;
  }
  &:hover {
    background-color:darken(#38cc70, 10%);
  }
}
.accordionTitleActive,
.accordionTitle.is-expanded {
   background-color:darken(#38cc70, 10%);
    &:before {

      transform:rotate(-225deg);
    }
}
.accordionItem {
    height:auto;
    overflow:hidden;
    //SHAME: magic number to allow the accordion to animate

     max-height:50em;
    transition:max-height 1s;


    @media screen and (min-width:48em) {
         max-height:15em;
        transition:max-height 0.5s

    }


}

.accordionItem.is-collapsed {
    max-height:0;
}
.no-js .accordionItem.is-collapsed {
  max-height: auto;
}
.animateIn {
     animation: accordionIn 0.45s normal ease-in-out both 1;
}
.animateOut {
     animation: accordionOut 0.45s alternate ease-in-out both 1;
}
@keyframes accordionIn {
  0% {
    opacity: 0;
    transform:scale(0.9) rotateX(-60deg);
    transform-origin: 50% 0;
  }
  100% {
    opacity:1;
    transform:scale(1);
  }
}

@keyframes accordionOut {
    0% {
       opacity: 1;
       transform:scale(1);
     }
     100% {
          opacity:0;
           transform:scale(0.9) rotateX(-60deg);
       }
}
