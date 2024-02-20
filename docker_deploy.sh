docker build . -t sous_chef_app
# docker run -p 8080:8080 -t -i -e OPENAI_API_KEY sous_chef_app:latest
gcloud config set run/region us-central1
docker tag sous_chef_app:latest us-central1-docker.pkg.dev/sous-chef-chat-ai/sous-chef-app/sous_chef_app
docker push us-central1-docker.pkg.dev/sous-chef-chat-ai/sous-chef-app/sous_chef_app
gcloud run deploy sous-chef-app --image=us-central1-docker.pkg.dev/sous-chef-chat-ai/sous-chef-app/sous_chef_app:latest