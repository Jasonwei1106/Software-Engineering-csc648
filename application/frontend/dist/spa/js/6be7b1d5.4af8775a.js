(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["6be7b1d5"],{"578a":function(t,e,a){"use strict";var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"q-pa-md bg-grey-3",staticStyle:{width:"30vw","max-width":"500px","min-width":"270px"}},[t._m(0),a("q-form",{on:{submit:t.onSubmit}},[a("div",[a("div",{staticClass:"q-mb-sm"},[a("q-input",{attrs:{dense:"",outlined:"","bg-color":"white",type:"text",placeholder:"USERNAME"},model:{value:t.logIn.username,callback:function(e){t.$set(t.logIn,"username",e)},expression:"logIn.username"}})],1),a("div",{staticClass:"q-mb-sm"},[a("q-input",{attrs:{dense:"",outlined:"","bg-color":"white",type:"password",placeholder:"PASSWORD"},model:{value:t.logIn.password,callback:function(e){t.$set(t.logIn,"password",e)},expression:"logIn.password"}})],1)]),a("div",{attrs:{align:"center"}},[a("div",{staticClass:"q-mb-md"},[a("q-btn",{staticClass:"full-width",attrs:{type:"submit",color:"primary",label:"LOG IN"}}),a("br")],1),a("router-link",{attrs:{to:"/forgot"}},[a("span",[t._v("FORGOT PASSWORD?")])]),a("br"),a("router-link",{attrs:{to:"/register"}},[a("span",{on:{click:t.emitClose}},[t._v("SIGN UP HERE!")])])],1)])],1)},o=[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{align:"center"}},[a("strong",[t._v("LOGIN")]),a("br"),a("br")])}],n=(a("7f7f"),a("bc3a")),i=a.n(n),r={components:{},data:function(){return{logIn:{}}},methods:{onSubmit:function(){var t=this;i.a.post("http://54.67.109.241:5000/api/login",{username:this.logIn.username,password:this.logIn.password}).then((function(e){t.$q.notify({icon:"done",color:"positive",message:"Welcome back!"}),t.$q.localStorage.set("__diyup__signedIn",e.data.token),t.$q.localStorage.set("__diyup__username",t.logIn.username),"rootHome"===t.$route.name?t.$router.go():t.$router.push({name:"rootHome"}).catch((function(e){e&&t.$router.go()})),t.emitClose()})).catch((function(){t.$q.notify({icon:"warning",color:"negative",message:"Something went wrong!"}),t.logIn={}}))},emitClose:function(){this.$emit("close")}}},c=r,l=a("2877"),u=Object(l["a"])(c,s,o,!1,null,null,null);e["a"]=u.exports},add6:function(t,e,a){t.exports=a.p+"img/DIY_Artwork.b5dfc94b.png"},f241:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("q-layout",{attrs:{view:"hHh lpR fFf"}},[s("q-header",{staticClass:"bg-primary text-white",attrs:{reveal:"",elevated:""}},[s("q-toolbar",[s("q-space"),s("div",{staticClass:"cursor-pointer",staticStyle:{width:"80px"},on:{click:function(e){return t.routeTo("rootHome")}}},[s("q-img",{attrs:{src:"../statics/icons/96p.png"}})],1),s("q-space"),s("div",{staticClass:"q-my-xs",staticStyle:{"max-width":"51vw"},attrs:{align:"center"}},[t.$q.localStorage.has("__diyup__signedIn")?s("div",[s("div",{staticClass:"row"},[s("div",{staticClass:"col"},[s("q-btn",{attrs:{dense:"",round:"",size:"md"},on:{click:function(e){t.leftDrawerOpen=!t.leftDrawerOpen}}},[s("q-avatar",{attrs:{size:"md","text-color":"white",icon:"person"}})],1)],1),s("q-separator",{attrs:{dark:"",vertical:""}}),s("div",{staticClass:"col"},[s("q-btn",{staticClass:"full-width",attrs:{flat:"","no-caps":"",label:"Log Out"},on:{click:t.logout}})],1)],1)]):s("div",[s("div",{staticClass:"row"},[s("div",{staticClass:"col"},[s("q-btn",{staticClass:"full-width",attrs:{flat:"","no-caps":"",label:"Log In"},on:{click:function(e){t.icon=!0}}})],1),s("q-separator",{attrs:{dark:"",vertical:""}}),s("div",{staticClass:"col"},[s("q-btn",{staticClass:"full-width",attrs:{flat:"","no-caps":"",label:"Sign Up",to:"/register"}})],1)],1)]),s("div",{staticClass:"row q-mt-xs"},[s("q-input",{staticClass:"col",attrs:{borderless:"",dense:"",outlined:"","bg-color":"white",color:"black",debounce:"300",placeholder:"Tutorial Title"},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.titleSearch(e)}},scopedSlots:t._u([{key:"append",fn:function(){return[""===t.filter?s("q-icon",{attrs:{name:"search"}}):s("q-icon",{staticClass:"cursor-pointer",attrs:{name:"clear"},on:{click:t.refreshSearch}})]},proxy:!0}]),model:{value:t.filter,callback:function(e){t.filter=e},expression:"filter"}})],1)])],1),t.$route.name&&"rootHome"===t.$route.name&&!t.leftDrawerOpen?s("q-toolbar",{staticClass:"bg-white text-black"},[s("q-toolbar-title",{staticClass:"row q-pa-md"},[s("div",{staticClass:"col",attrs:{align:"center"}},[s("strong",{staticClass:"gt-sm",staticStyle:{"font-size":"1.5em",position:"relative",top:"15%",transform:"translateY(-50%)"}},[t._v("\n            STEP-BY-STEP PROJECTS BY USERS FOR USERS\n          ")]),s("strong",{staticClass:"sm",staticStyle:{"font-size":"1em",position:"relative",top:"20%",transform:"translateY(-50%)"}},[t._v("\n            STEP-BY-STEP PROJECTS BY USERS FOR USERS\n          ")]),s("strong",{staticClass:"lt-sm",staticStyle:{"font-size":".6em"}},[t._v("\n            STEP-BY-STEP PROJECTS BY USERS FOR USERS\n          ")])]),s("img",{staticClass:"col-2 q-mr-md gt-xs",staticStyle:{width:"10%","max-width":"100px","max-height":"70px"},attrs:{src:a("add6")}})])],1):t._e()],1),s("q-drawer",{attrs:{bordered:"",overlay:"","content-class":"bg-grey-2"},model:{value:t.leftDrawerOpen,callback:function(e){t.leftDrawerOpen=e},expression:"leftDrawerOpen"}},[s("q-list",[s("q-item-label",{attrs:{header:""}},[s("div",{staticClass:"row"},[t._v("\n          Navigation\n          "),s("q-space"),s("q-btn",{attrs:{flat:"",dense:"",round:"",icon:"close"},on:{click:function(e){t.leftDrawerOpen=!t.leftDrawerOpen}}})],1)]),s("q-item",{attrs:{to:"/",exact:""}},[s("q-item-section",{attrs:{avatar:""}},[s("q-icon",{attrs:{name:"list"}})],1),s("q-item-section",[s("q-item-label",[t._v("Home")])],1)],1),s("q-item",{attrs:{to:"/tutorials/"+t.$q.localStorage.getItem("__diyup__username"),exact:""}},[s("q-item-section",{attrs:{avatar:""}},[s("q-icon",{attrs:{name:"where_to_vote"}})],1),s("q-item-section",[s("q-item-label",[t._v("My Tutorials")])],1)],1)],1)],1),s("q-page-container",{staticStyle:{"min-height":"90vh"}},[s("router-view")],1),s("div",{staticStyle:{"background-color":"#027BE3",height:"100px"}},[s("div",{staticClass:"row",staticStyle:{width:"96%",margin:"0 auto"}},[s("div",{staticClass:"q-pa-md"},[s("q-img",{staticStyle:{width:"70px"},attrs:{src:"../statics/icons/96p.png"}})],1),s("q-space"),s("div",{staticClass:"q-pa-md",attrs:{align:"center"}},[s("div",{staticClass:"text-white cursor-pointer",on:{click:function(e){return t.routeTo("rootAbout")}}},[t._v("\n          About Us\n        ")])]),s("div",{staticClass:"q-pa-md",attrs:{align:"center"}},[s("div",{staticClass:"text-white"},[t._v("\n          Follow Us On\n        ")]),s("div",[s("q-icon",{staticClass:"cursor-pointer",attrs:{name:"fab fa-facebook-square",size:"2rem"},on:{click:function(e){return t.goTo("https://www.facebook.com")}}}),s("q-icon",{staticClass:"cursor-pointer",attrs:{name:"fab fa-instagram",size:"2rem"},on:{click:function(e){return t.goTo("https://www.instagram.com/")}}}),s("q-icon",{staticClass:"cursor-pointer",attrs:{name:"fab fa-twitter-square",size:"2rem"},on:{click:function(e){return t.goTo("https://twitter.com/")}}})],1)])],1)]),s("q-dialog",{model:{value:t.icon,callback:function(e){t.icon=e},expression:"icon"}},[s("q-card",[s("LogIn",{on:{close:function(e){t.icon=!1}}})],1)],1)],1)},o=[],n=(a("7f7f"),a("578a")),i={name:"MyLayout",components:{LogIn:n["a"]},created:function(){},updated:function(){},data:function(){return{leftDrawerOpen:!1,icon:!1,filter:""}},methods:{refreshSearch:function(){this.filter="",this.titleSearch(event)},titleSearch:function(t){t.target.value?this.$router.push("/?title=".concat(t.target.value)).catch((function(t){})):this.$router.push("/").catch((function(t){}))},goTo:function(t){window.location.href=t},routeTo:function(t){this.$router.push({name:t}).catch((function(){}))},logout:function(){this.$q.localStorage.remove("__diyup__signedIn"),this.$q.localStorage.remove("__diyup__username"),"rootHome"===this.$route.name?this.$router.go():this.$router.push({name:"rootHome"}).catch((function(t){}))}}},r=i,c=a("2877"),l=Object(c["a"])(r,s,o,!1,null,null,null);e["default"]=l.exports}}]);