(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["df3716e2"],{"578a":function(t,e,o){"use strict";var n=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"q-pa-md bg-grey-3",staticStyle:{width:"30vw","max-width":"500px","min-width":"270px"}},[t._m(0),o("q-form",{on:{submit:t.onSubmit}},[o("div",[o("div",{staticClass:"q-mb-sm"},[o("q-input",{attrs:{dense:"",outlined:"","bg-color":"white",type:"text",placeholder:"USERNAME"},model:{value:t.logIn.username,callback:function(e){t.$set(t.logIn,"username",e)},expression:"logIn.username"}})],1),o("div",{staticClass:"q-mb-sm"},[o("q-input",{attrs:{dense:"",outlined:"","bg-color":"white",type:"password",placeholder:"PASSWORD"},model:{value:t.logIn.password,callback:function(e){t.$set(t.logIn,"password",e)},expression:"logIn.password"}})],1)]),o("div",{attrs:{align:"center"}},[o("div",{staticClass:"q-mb-md"},[o("q-btn",{staticClass:"full-width",attrs:{type:"submit",color:"primary",label:"LOG IN"}}),o("br")],1),o("router-link",{attrs:{to:"/forgot"}},[o("span",[t._v("FORGOT PASSWORD?")])]),o("br"),o("router-link",{attrs:{to:"/register"}},[o("span",{on:{click:t.emitClose}},[t._v("SIGN UP HERE!")])])],1)])],1)},a=[function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{attrs:{align:"center"}},[o("strong",[t._v("LOGIN")]),o("br"),o("br")])}],i=(o("7f7f"),o("bc3a")),r=o.n(i),s={components:{},data:function(){return{logIn:{}}},methods:{onSubmit:function(){var t=this;r.a.post("http://54.67.109.241:5000/api/login",{username:this.logIn.username,password:this.logIn.password}).then((function(e){t.$q.notify({icon:"done",color:"positive",message:"Welcome back!"}),t.$q.localStorage.set("__diyup__signedIn",e.data.token),t.$q.localStorage.set("__diyup__username",t.logIn.username),"rootHome"===t.$route.name?t.$router.go():t.$router.push({name:"rootHome"}).catch((function(e){e&&t.$router.go()})),t.emitClose()})).catch((function(){t.$q.notify({icon:"warning",color:"negative",message:"Something went wrong!"}),t.logIn={}}))},emitClose:function(){this.$emit("close")}}},l=s,c=o("2877"),u=Object(c["a"])(l,n,a,!1,null,null,null);e["a"]=u.exports},"6d45":function(t,e,o){},"8b24":function(t,e,o){"use strict";o.r(e);var n=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("q-page",{staticClass:"q-pa-sm"},[o("div",{staticClass:"q-pa-md"},[o("MockTable")],1)])},a=[],i=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",[o("q-table",{attrs:{flat:"","hide-header":"","wrap-cells":"",separator:"none","row-key":"title",data:t.curData,columns:t.columns,filter:t.option.value,pagination:t.pagination},on:{"update:pagination":function(e){t.pagination=e}},scopedSlots:t._u([{key:"top-left",fn:function(){return[t.$q.localStorage.has("__diyup__signedIn")?o("q-btn",{attrs:{outline:"",label:"Create a new project"},on:{click:t.goToPost}}):o("q-btn",{attrs:{outline:"",label:"Please sign in to create tutorials"},on:{click:function(e){t.icon=!0}}})]},proxy:!0},{key:"top-right",fn:function(){return[o("q-toolbar",[""!==t.option?o("q-btn",{staticClass:"q-mr-sm",attrs:{flat:"",dense:"",round:"",icon:"close"},on:{click:function(e){t.option=""}}}):t._e(),o("q-select",{staticClass:"col-4",staticStyle:{"min-width":"200px"},attrs:{outlined:"",dense:"",label:"Category Filter","bg-color":"white",color:"black",options:t.categories},model:{value:t.option,callback:function(e){t.option=e},expression:"option"}})],1)]},proxy:!0},{key:"body",fn:function(e){return[o("q-tr",{attrs:{props:e}},[o("q-td",{key:"title",attrs:{colspan:"100%",props:e}},[o("q-card",{staticClass:"q-pa-md",staticStyle:{"min-height":"15vh"}},[o("div",{staticClass:"row cursor-pointer",on:{click:function(o){return t.routeToTutorial(e.row)}}},[o("div",{staticClass:"col-4",attrs:{align:"center"}},[o("q-img",{staticStyle:{"max-height":"140px","max-width":"150px"},attrs:{src:"https://placeimg.com/500/300/nature?t="+Math.random(),"spinner-color":"primary"}})],1),o("div",{staticClass:"col gt-xs"},[o("b",[t._v("Title:")]),t._v("\n                "+t._s(e.row.title)+" by "+t._s(e.row.author_username)),o("br"),o("b",[t._v("Author's Difficulty Rating:")]),t._v("\n                "+t._s(e.row.author_difficulty)),o("br"),o("b",[t._v("Users' Rating:")]),o("q-rating",{staticClass:"q-pl-sm",attrs:{readonly:"",size:"1.5em",icon:"thumb_up",value:"None"===e.row.rating?5:Number(e.row.rating)}}),o("br"),o("b",[t._v("Category:")]),t._v("\n                "+t._s(e.row.category)),o("br")],1),o("div",{staticClass:"col-5 q-pr-xl gt-xs",attrs:{align:"left"}},[o("b",[t._v("Description:")]),t._v(" "+t._s(e.row.description)+"\n              ")]),o("div",{staticClass:"col q-pl-xs xs",attrs:{align:"left"}},[o("b",[t._v("Title:")]),t._v("\n                "+t._s(e.row.title)+" by "+t._s(e.row.author_username)+"\n                "),o("br"),o("b",[t._v("Description:")]),t._v(" "+t._s(e.row.description)+"\n              ")])])])],1)],1)]}}])}),o("q-dialog",{model:{value:t.icon,callback:function(e){t.icon=e},expression:"icon"}},[o("q-card",[o("LogIn",{on:{close:function(e){t.icon=!1}}})],1)],1)],1)},r=[],s=(o("6762"),o("2fdb"),o("bc3a")),l=o.n(s),c=o("578a"),u={watch:{$route:"titleQueryFilter"},components:{LogIn:c["a"]},created:function(){this.fetchData(),this.filter=this.$route.query.title||""},data:function(){return{icon:!1,filter:"",categories:[{label:"Electronics",value:"electronics"},{label:"Coding",value:"coding"},{label:"Robotics",value:"robotics"},{label:"Cooking",value:"cooking"},{label:"Crafts",value:"crafts"},{label:"Home & Decor",value:"homeDecor"},{label:"Testing",value:"testing"}],option:"",columns:[{name:"title",label:"Title",required:!0,align:"left",field:function(t){return t.title},format:function(t){return"".concat(t)},sortable:!0},{name:"category",label:"Category",required:!0,align:"left",field:function(t){return t.category},format:function(t){return"".concat(t)},sortable:!0}],data:[],curData:[],pagination:{rowsPerPage:10,sortBy:"title",descending:!1}}},methods:{routeToTutorial:function(t){this.$router.push("/tutorial/".concat(t.uuid))},titleQueryFilter:function(){var t=this;this.filter=this.$route.query.title,this.filter?this.curData=this.data.filter((function(e){return e.title.toLowerCase().includes(t.filter.toLowerCase())})):this.curData=this.data},fetchData:function(){var t=this;l.a.get("http://54.67.109.241:5000/api/tutorial/get").then((function(e){t.data=e.data.tutorials,t.data.forEach((function(e){t.curData.push(e)}))}))},goToPost:function(){this.$q.localStorage.has("__diyup__signedIn")&&this.$router.push({path:"/post"}).catch((function(t){}))}}},d=u,p=(o("e0b8"),o("2877")),f=Object(p["a"])(d,i,r,!1,null,null,null),g=f.exports,m={name:"PageIndex",components:{MockTable:g},created:function(){this.setPageTab()},beforeUpdate:function(){this.setPageTab()},data:function(){return{filter:""}},methods:{setPageTab:function(){this.$route.path}}},b=m,h=Object(p["a"])(b,n,a,!1,null,null,null);e["default"]=h.exports},e0b8:function(t,e,o){"use strict";var n=o("6d45"),a=o.n(n);a.a}}]);