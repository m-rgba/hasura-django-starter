<script>
    import { onMount } from "svelte";
	import { authToken } from './stores/auth.js'
    import { token, authSuccess } from "../App.svelte"

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

    onMount(() => {

    });

    function getUsers() {
        const request = await fetch("http://localhost:8000/api/user/reset_password/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify({ email }),
        });
        if (request.ok) {
            successMessage = 'We\'ve sent you an email to confirm your account. Selecting the link from your email will allow you to reset the password to your account.';
        } else {
            errorMessage = 'It looks like there was a problem. This could be because that email isn\'t associated with any accounts in our system. Please try again.';
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