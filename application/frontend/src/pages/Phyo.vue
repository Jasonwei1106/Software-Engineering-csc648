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
              src="../statics/square_phyo.jpg"
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

    <div style="padding: 40px; margin: 100px">
      {{ intro }}
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      intro: `Hi, I'm Phyo Htut. I'm currently a graduate student for Energy Systems [MS] and in process of transferring to Computer Science [MS] at San Francisco State University (SFSU). I am the project lead for this class project.`
    }
  }
}
</script>

<style>

</style>
