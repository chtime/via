# Resources

This directory contains various Kubernetes/OpenShift resources. To run the `via` application from this repository, you don't need any of those - you can have OpenShift create them for you using the "Add / Import from Git" functionality.

OpenShift will then create these resources (also found for reference in `./generated-reference`):

- Deployment
- Service
- Route
- BuildConfig
- ImageStream

The magic here is that (when using the UI defaults):
1. the BuildConfig will build this project's Dockerfile
2. publish the image in the cluster's registry
3. register that image in an imagestream
4. and the deployment will be updated due to a `image.openshift.io/triggers` annotation to use the new image
5. the usual kuberentes reconciliation will take place

## Configuring Auto-Builds through Webhooks

The BuildConfig will furthermore have triggers for webhooks; in order to call these webhooks from e.g. GitHub, you need to extract their URL. Either you check the web-console buildconfig and "Copy URL with secret" for the GitHub webhook, or you assemble the URL manually yourself:

```bash
oc get buildconfig/via # note the Webhook URL
```

You'll see a placeholder in the URL "`<secret>`" - you need to replace this with the corresponding secret value, e.g. 
```bash
kubectl get secrets/via-github-webhook-secret --template={{.data.WebHookSecretKey}} | base64 -d
```

In the end, you'll get an URL like this:
```
https://api.demo.a-cluster.ch:6443/apis/build.openshift.io/v1/namespaces/time/buildconfigs/via/webhooks/0d9d5118dc5526fe/github
```
You register this in your repo's webhook list using JSON as content-type.

In addition you need to allow anonymous external "users" to trigger builds without additional authentication besides the obfuscated URL - you add a RoleBinding for this namespace to bind `system:unauthenticated` to the `system:webhook` ClusterRole. See `webhook-anon-access.yaml`.

Any pushes to the repository should now trigger builds and new deployments.

