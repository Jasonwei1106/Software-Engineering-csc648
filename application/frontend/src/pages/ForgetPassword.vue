<template>
  <q-card class="q-pa-md" style="width: 98%; margin: 1em auto;">
    <strong>Reset Password</strong>
    <hr>
    <q-form @submit="onSubmit">
      <div class="q-pa-md">

        <div>
          <strong>Email:</strong>
          <q-input
            dense filled
            type="text"
            placeholder="Email..."
            v-model="logIn.name"
            required
          >
            <template v-slot:prepend>
              <q-icon name="mail" />
            </template>
          </q-input>
        </div>

        <div>
          <strong>Password:</strong>
          <q-input
            dense filled
            type="password"
            placeholder="Password..."
            v-model="logIn.password"
            required
          >
            <template v-slot:prepend>
              <q-icon name="vpn_key" />
            </template>
          </q-input>
        </div>

        <div>
          <strong>Confirm Password:</strong>
          <q-input
            dense filled
            type ="password"
            placeholder="Password..."
            v-model="logIn.conpassword"
            required
          >
            <template v-slot:prepend>
              <q-icon name="vpn_key" />
            </template>
          </q-input>
        </div>
      </div>

      <div class="q-gutter-sm" align="center" >
        <q-btn no-caps type="submit" color="primary" label="Confirm" />
      </div>
    </q-form>
  </q-card>
</template>

<script>
export default {
  data () {
    return {
      logIn: {}
    }
  },
  methods: {
    onSubmit: function () {
      this.logIn = {}
    }
  }
}
</script>
