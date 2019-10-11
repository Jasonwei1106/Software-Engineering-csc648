<template>
  <q-card class="q-pa-md" style="width: 98%; margin: 1em auto;">
    <strong>Register</strong>
    <hr>
    <q-form @submit.prevent.stop="onSubmit">
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

      <div class="q-gutter-sm">
        <q-checkbox
        v-model="accept"
        label="Do you agree?"
      />
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
      accept: 'no',
      logIn: {}
    }
  },
  methods: {
    onSubmit: function () {
      if (this.accept !== true) {
        this.$q.notify({
          color: 'negative',
          message: 'You need to accept the license and terms first'
        })
      } else {
        this.$q.notify({
          icon: 'done',
          color: 'positive',
          message: 'Submitted'
        })
        this.logIn = {}
      }
    }
  }
}
</script>
