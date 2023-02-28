<script lang="ts">
  import Buttons from "./lib/Buttons.svelte";
  import tags from "./assets/tag.json";
  let count = 0;
  const post = (sentiment: string, text: string) => {
    count += 1;
    return fetch(`http://localhost:8080/${sentiment}`, {
      method: "POST",
      body: JSON.stringify(text),
      headers: { "Content-Type": "application/json" },
    });
  };
</script>

<main>
  <div>
    <h1>{tags[count].text}</h1>
    <h2>{count}</h2>
    <div class="card">
      <Buttons {post} tag={tags[count].text} />
    </div>
  </div>
</main>

<style>
</style>
