<script>
    import { onMount } from "svelte";
	import { authToken } from '../stores/auth.js'
    import { token, authSuccess } from "../App.svelte"

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

    onMount(() => {

    });

    async function getUsers() {
        const query = `
        `;
        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
                Authorization: "Bearer: " + $authToken
            },
            body: JSON.stringify({ email }),
        });
        if (request.ok) {
        } else {
        }
    }
</script>

<Header />

<content>
    <div class="container pt-xl mb-xl">
        <div class="row">
            <div class="col-12 mb-sm">
                <h1>Users</h1>
            </div>
            <div class="col-12">
                <p class="muted">[ Placeholder for your content ]</p>
            </div>
        </div>
    </div>
</content>

<Footer />