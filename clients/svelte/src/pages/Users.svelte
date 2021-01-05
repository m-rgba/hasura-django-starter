<script>
    import { onMount } from "svelte";
	import { authToken } from '../stores/auth.js'
    // import { token, authSuccess } from "../App.svelte"

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

    onMount(() => {
        getUsersAdmin();
    });

    async function getUsersAdmin() {
        const query = JSON.stringify({
            query: `
                query allUsers {
                    auth_user {
                        id
                        username
                        email
                        is_active
                        api_profile {
                            role
                        }
                    }
                }
            `
            });
        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
                Authorization: "Bearer " + $authToken,
            },
            body: query
        });
        if (request.ok) {
            const response = await request.json();
            console.log(response)
        } else {
            console.log('Query Error...')
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