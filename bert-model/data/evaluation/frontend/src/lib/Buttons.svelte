<script lang="ts">
  export let post: (sentiment: string, text: string) => Promise<Response>;
  export let tag: string;

  const positive = () => post("positive", tag);
  const neutral = () => post("neutral", tag);
  const negative = () => post("negative", tag);
  const wish = () => post("wish", tag);
</script>

<button on:click={() => positive()}> Positive </button>
<button on:click={neutral}> Neutral </button>
<button on:click={negative}> Negative </button>
<button on:click={wish}> Wish </button>
