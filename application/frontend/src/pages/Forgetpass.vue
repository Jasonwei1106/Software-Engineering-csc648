<template>
  <div class="q-pa-md">
    <strong>Reset Password</strong>
    <hr>
    <q-form @submit="onSubmit">
      <div class="q-pa-md">
        <div class="row">
          <q-input
            type="text"
            placeholder="username here plz..."
            prefix="Username:"
            v-model="logIn.name"
          >
            <template v-slot:prepend>
              <q-icon name="mail" />
            </template>
          </q-input>
        </div>
        <div class="row">
          <q-input
            type="password"
            placeholder="password..."
            prefix="Password:"
            v-model="logIn.password"
          >
            <template v-slot:prepend>
              <q-icon name="vpn_key" />
            </template>
          </q-input>
        </div>
        <div class ="row">
          <q-input
          type ="password"
          placeholder="confirm your password"
          prefix="Confirm password:"
          v-model="logIn.conpassword">
          <template v-slot:prepend>
              <q-icon name="vpn_key" />
            </template>
            </q-input>
      </div>
      </div>

      <div class="row q-gutter-sm">
        <q-btn no-caps type="submit" to="/" v-close-popup >Confirm</q-btn>
      </div>
    </q-form>
        <q-dialog v-model="forgetpass">
         <q-card>
           <Register @close="forgetpass = false" />
         </q-card>
        </q-dialog>
  </div>
</template>

<script>
export default {
  data () {
    return {
      logIn: {},
      forgetpass: false
    }
  },
  methods: {
    onSubmit: function () {
      this.logIn = {}
    }
  }
}
</script>
