(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["2d0ba83f"],{3815:function(e,t,o){"use strict";o.r(t);var n=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"q-pa-md",staticStyle:{width:"98%",margin:"1em auto"}},[o("strong",[e._v("Reset Password")]),o("q-stepper",{ref:"stepper",attrs:{vertical:"",animated:"","active-color":"purple"},scopedSlots:e._u([{key:"navigation",fn:function(){return[o("q-stepper-navigation",[o("q-btn",{attrs:{color:"deep-orange",label:4===e.step?"Finish":"Continue"},on:{click:e.onSubmit}}),e.step>1?o("q-btn",{staticClass:"q-ml-sm",attrs:{flat:"",color:"deep-orange",label:"Back"},on:{click:function(t){return e.$refs.stepper.previous()}}}):e._e()],1)]},proxy:!0}]),model:{value:e.step,callback:function(t){e.step=t},expression:"step"}},[o("q-step",{attrs:{name:1,prefix:"1",title:"Type your email"}},[o("div",[o("strong",[e._v("Email:")]),o("q-input",{staticStyle:{"max-width":"600px"},attrs:{dense:"",filled:"",type:"text",placeholder:"Email..."},scopedSlots:e._u([{key:"prepend",fn:function(){return[o("q-icon",{attrs:{name:"mail"}})]},proxy:!0}]),model:{value:e.logIn.name,callback:function(t){e.$set(e.logIn,"name",t)},expression:"logIn.name"}})],1)]),o("q-step",{attrs:{name:2,prefix:"2",title:"Type your code"}},[o("div",[o("strong",[e._v("Code:")]),o("q-input",{staticStyle:{"max-width":"200px"},attrs:{dense:"",filled:"",type:"text",placeholder:"confirm code..."},scopedSlots:e._u([{key:"prepend",fn:function(){return[o("q-icon",{attrs:{name:"confirmation_number"}})]},proxy:!0}]),model:{value:e.logIn.code,callback:function(t){e.$set(e.logIn,"code",t)},expression:"logIn.code"}})],1)]),o("q-step",{attrs:{name:3,prefix:"3",title:"Reset your new password"}},[o("div",[o("strong",[e._v("Password:")]),o("q-input",{staticStyle:{"max-width":"600px"},attrs:{dense:"",filled:"",type:"password",placeholder:"Password..."},scopedSlots:e._u([{key:"prepend",fn:function(){return[o("q-icon",{attrs:{name:"vpn_key"}})]},proxy:!0}]),model:{value:e.logIn.password,callback:function(t){e.$set(e.logIn,"password",t)},expression:"logIn.password"}})],1)]),o("q-step",{attrs:{name:4,prefix:"4",title:"Confirm your new password"}},[o("div",[o("strong",[e._v("Confirm Password:")]),o("q-input",{staticStyle:{"max-width":"600px"},attrs:{dense:"",filled:"",type:"password",placeholder:"Password..."},scopedSlots:e._u([{key:"prepend",fn:function(){return[o("q-icon",{attrs:{name:"vpn_key"}})]},proxy:!0}]),model:{value:e.logIn.conpassword,callback:function(t){e.$set(e.logIn,"conpassword",t)},expression:"logIn.conpassword"}})],1)])],1)],1)},s=[],r=(o("8e6e"),o("8a81"),o("ac6a"),o("cadf"),o("06db"),o("456d"),o("c47a")),a=o.n(r),i=(o("7f7f"),o("bc3a")),p=o.n(i);function c(e,t){var o=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),o.push.apply(o,n)}return o}function l(e){for(var t=1;t<arguments.length;t++){var o=null!=arguments[t]?arguments[t]:{};t%2?c(Object(o),!0).forEach((function(t){a()(e,t,o[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(o)):c(Object(o)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(o,t))}))}return e}var d={data:function(){return{step:1,logIn:{name:"",password:"",code:"",conpassword:""},previousLog:{name:"",password:"",conpassword:""}}},methods:{onSubmit:function(){var e=this;1===this.step&&this.logIn.name.length<1?this.$q.notify({message:"Please your email here"}):3===this.step&&this.logIn.password.length<1?this.$q.notify({message:"Please enter password here"}):4===this.step&&this.logIn.password!==this.logIn.conpassword?this.$q.notify({message:"Your confirm password doesn't match"}):(1===this.step&&p.a.post("http://54.67.109.241:5000/api/user/forgot/send",{email_address:this.logIn.name}).then((function(t){e.$q.notify({icon:"done",color:"positive",message:"Check your email for the verify code"})})).catch((function(t){t&&e.$q.notify({icon:"warning",color:"negative",message:"Your account does not exsist!"})})),2===this.step&&p.a.post("http://54.67.109.241:5000/api/user/forgot/verify",{email_address:this.logIn.name,password_reset_code:this.logIn.code}).then((function(t){e.$q.notify({icon:"done",color:"positive",message:"submitted"})})).catch((function(t){t&&e.$q.notify({icon:"warning",color:"negative",message:"Verfied code is wrong"})})),4===this.step&&p.a.post("http://54.67.109.241:5000/api/user/forgot/reset",{email_address:this.logIn.name,password:this.logIn.conpassword}).then((function(t){e.$q.notify({icon:"done",color:"positive",message:"reset your password"}),e.$router.push({name:"rootHome"})})).catch((function(t){t&&e.$q.notify({icon:"warning",color:"negative",message:"Something went wrong!"})})),this.step++,this.previousLog=l({},this.logIn))},onBack:function(){this.logIn=l({},this.previousLog)}}},u=d,f=o("2877"),m=Object(f["a"])(u,n,s,!1,null,null,null);t["default"]=m.exports}}]);