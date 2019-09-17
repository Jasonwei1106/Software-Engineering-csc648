<template>
  <div>
    <div>
      <q-card>
        <q-card-section>
          <q-avatar
            size="200px"
            style="
              padding-top: 40px;
              margin-left: 42%;
            "
          >
            <q-img
              src="../statics/myles.jpg"
              class="avatar"
              style="
                max-width: 400px;
                height: 200px;
              "
            />
          </q-avatar>
        </q-card-section>
      </q-card>
    </div>

    <div style="padding: 40px; margin: 100px;">
      {{ intro }}
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      intro: `Hello, my name is Myles. Currently I am a graduate student in Embedded Electrical and Computer Systems. I enjoy cooking and bouldering.`
    }
  }
}
</script>

<style>

</style>
