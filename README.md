# github_action_ci_workflow




details explanation:

```
name: CI/CD                                                                   # ওয়ার্কফ্লোর নাম নির্ধারণ

on:                                                                           # ইভেন্ট নির্ধারণ যা ওয়ার্কফ্লো ট্রিগার করবে
  push:                                                                       # পুশ ইভেন্টের জন্য
    branches:                                                                 # শাখা নির্ধারণ
      - main                                                                  # প্রধান শাখায় পুশ করলে ট্রিগার হবে

jobs:                                                                         # জবসমূহের তালিকা
  ci_part:                                                                    # সিআই অংশের জব আইডি
    name: Build & Push Docker Image                                          # জবের নাম
    runs-on: ubuntu-latest                                                    # উবুন্টু লেটেস্ট রানারে জব চলবে

    steps:                                                                    # স্টেপসমূহের তালিকা
      - name: Checkout source code                                           # সোর্স কোড চেকআউট করার ধাপ
        uses: actions/checkout@v4                                            # রিপোজিটরির কোড ওয়ার্কস্পেসে আনে

      - name: Set up Docker Buildx                                           # ডকার বিল্ডএক্স সেটআপ করার ধাপ
        uses: docker/setup-buildx-action@v3                                 # উন্নত ডকার বিল্ড ফিচার সক্রিয় করে (মাল্টি-আর্কিটেকচার, ক্যাশিং)

      - name: Login to Docker Hub                                            # ডকার হাবে লগইন করার ধাপ
        uses: docker/login-action@v3                                         # ডকার হাবে অথেনটিকেট করার জন্য
        with:                                                                 # ইনপুট প্যারামিটার
          username: ${{ secrets.DOCKER_USERNAME }}                           # ডকার হাব ইউজারনেম সিক্রেট থেকে নেওয়া
          password: ${{ secrets.DOCKER_PASSWORD }}                           # ডকার হাব পাসওয়ার্ড/টোকেন সিক্রেট থেকে নেওয়া

      - name: Build Docker image                                             # ডকার ইমেজ বিল্ড করার ধাপ
        run: |                                                               # শেল কমান্ড চালানোর জন্য
          docker build -t ${{ secrets.DOCKER_USERNAME }}/fastapi-demo:latest .  # Dockerfile থেকে ইমেজ বিল্ড করে ট্যাগ দেয়

      - name: Push Docker image                                              # ডকার ইমেজ পুশ করার ধাপ
        run: |                                                               # শেল কমান্ড চালানোর জন্য
          docker push ${{ secrets.DOCKER_USERNAME }}/fastapi-demo:latest      # বিল্ডকৃত ইমেজ ডকার হাবে আপলোড করে

  cd_part:                                                                    # সিডি অংশের জব আইডি
    name: Deploy to Server                                                    # জবের নাম
    needs: ci_part                                                            # ci_part শেষ হলে এই জব চলবে
    runs-on: ubuntu-latest                                                    # উবুন্টু লেটেস্ট রানারে জব চলবে

    steps:                                                                    # স্টেপসমূহের তালিকা
      - name: Deploy via SSH                                                 # SSH এর মাধ্যমে ডিপ্লয় করার ধাপ
        uses: appleboy/ssh-action@v1.2.0                                    # SSH দিয়ে সার্ভারে কমান্ড চালানোর অ্যাকশন
        with:                                                                 # ইনপুট প্যারামিটার
          host: ${{ secrets.SERVER_HOST }}                                   # সার্ভারের আইপি বা ডোমেইন সিক্রেট থেকে
          username: ${{ secrets.SERVER_USERNAME }}                           # সার্ভারের ইউজারনেম সিক্রেট থেকে
          key: ${{ secrets.SERVER_SSH_KEY }}                                 # সার্ভারের SSH প্রাইভেট কী সিক্রেট থেকে

          script: |                                                          # সার্ভারে চালানোর স্ক্রিপ্ট
            docker pull ${{ secrets.DOCKER_USERNAME }}/fastapi-demo:latest   # ডকার হাব থেকে সর্বশেষ ইমেজ ডাউনলোড করে

            docker stop fastapi-demo || true                                 # পুরোনো কন্টেইনার থামায় (না থাকলে এরর ইগনোর)

            docker rm fastapi-demo || true                                   # পুরোনো কন্টেইনার মুছে ফেলে (না থাকলে এরর ইগনোর)

            docker run -d --name fastapi-demo --restart unless-stopped -p 8000:8000 ${{ secrets.DOCKER_USERNAME }}/fastapi-demo:latest
                                                                              # নতুন কন্টেইনার ব্যাকগ্রাউন্ডে চালায়, অটো-রিস্টার্ট সক্রিয়, এবং পোর্ট ৮০০০ ম্যাপ করে
```


# 📘 প্রতিটি অ্যাকশনের বিস্তারিত ব্যাখ্যা:

### 🔹 actions/checkout@v4
- কাজ: আপনার গিটহাব রিপোজিটরির কোড ওয়ার্কস্পেসে ক্লোন করে আনে।

- কারণ: পরবর্তী ধাপগুলোতে Dockerfile এবং অন্যান্য ফাইল ব্যবহার করার জন্য কোডের প্রয়োজন।

### 🔹 docker/setup-buildx-action@v3
- কাজ: Docker Buildx সেটআপ করে, যা Docker-এর উন্নত বিল্ডিং ফিচার।

- কারণ: Buildx দিয়ে আপনি মাল্টি-আর্কিটেকচার ইমেজ বিল্ড করতে পারেন, বিল্ড ক্যাশ ব্যবহার করতে পারেন, এবং আরও দ্রুত বিল্ড করতে পারেন। এটা সাধারণ docker build-এর আপগ্রেড ভার্সন।

### 🔹 docker/login-action@v3
- কাজ: Docker Hub-এ লগইন করে।

- কারণ: ইমেজ পুশ করার আগে Docker Hub-এ অথেনটিকেট হওয়া প্রয়োজন, যাতে আপনার অ্যাকাউন্টে ইমেজ আপলোড করতে পারেন।

### 🔹 docker/build (run)
- কাজ: Dockerfile থেকে Docker ইমেজ তৈরি করে।

- কারণ: আপনার অ্যাপ্লিকেশন কোড থেকে একটি চলমান কন্টেইনার ইমেজ তৈরি করতে হবে যা ডিপ্লয় করা যাবে।

### 🔹 docker/push (run)
- কাজ: বিল্ডকৃত ইমেজ Docker Hub-এ আপলোড করে।

- কারণ: ইমেজটি রেজিস্ট্রিতে সংরক্ষণ করতে হবে যাতে পরে সার্ভার থেকে ডাউনলোড করা যায়।

### 🔹 appleboy/ssh-action@v1.2.0
- কাজ: SSH প্রোটোকল ব্যবহার করে রিমোট সার্ভারে সংযোগ করে এবং কমান্ড চালায়।

- কারণ: সার্ভারে ডকার কমান্ড চালানোর মাধ্যমে অ্যাপ্লিকেশন ডিপ্লয় করতে হয়। এই অ্যাকশনটি সরাসরি সার্ভারে কমান্ড এক্সিকিউট করার সুবিধা দেয়।

--- 
💡 প্রতিটি স্টেপের কাজ: CI অংশ ইমেজ বিল্ড করে পুশ করে, আর CD অংশ সার্ভারে গিয়ে সেই ইমেজ ডাউনলোড করে কন্টেইনার চালু করে।
































লোকালভাবে FastAPI app run করে test  তাহলে:

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

