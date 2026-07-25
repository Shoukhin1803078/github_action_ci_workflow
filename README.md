# github_action_ci_workflow

হ্যাঁ, যদি তুমি লোকালভাবে FastAPI app run করে test করতে চাও, তাহলে:

- ```docker compose up --build```

অথবা যদি compose file-এর নাম docker-compose.dev.yml হয়:

- ```docker compose -f docker-compose.dev.yml up --build```
কিন্তু যদি তোমার goal CI practice হয় (Build → Login → Push)

তাহলে docker compose ব্যবহার করার দরকার নেই।

CI-তে সাধারণত docker build ব্যবহার করা হয়, কারণ CI-এর উদ্দেশ্য হচ্ছে image তৈরি করা এবং registry-তে push করা।

লোকালি CI-এর প্রতিটি step এভাবে practice করতে পারো:

1. Build Image
- ```docker build -t fastapi-demo .```

Check:

docker images
2. Login to Docker Hub
```docker login```

অথবা Access Token দিয়ে:

```docker login -u YOUR_DOCKER_USERNAME```

তারপর Access Token paste করবে।

3. Tag Image
```docker tag fastapi-demo YOUR_DOCKER_USERNAME/fastapi-demo:latest```
4. Push Image
```docker push YOUR_DOCKER_USERNAME/fastapi-demo:latest```
যদি app-টাও run করে দেখতে চাও
docker run -p 8000:8000 fastapi-demo

তারপর browser-এ:

http://localhost:8000

অথবা:

curl http://localhost:8000
সংক্ষেপে
App run/test করতে: docker compose up --build (বা docker run)
CI practice করতে: docker build → docker login → docker tag → docker push

CI workflow-তে docker compose সাধারণত ব্যবহার করা হয় না, কারণ compose মূলত একাধিক container একসাথে চালানোর জন্য, image build ও registry push করার জন্য নয়।