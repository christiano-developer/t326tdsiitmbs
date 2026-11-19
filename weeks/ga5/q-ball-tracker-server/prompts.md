# Prompts — q-ball-tracker-server

1. Read the grader: frames come from `/questionData` as length-prefixed PNGs; downloaded with the session's quizSign.
2. First detector (distance transform peaks, then disk correlation): wrong counts (99–108). *Failure.*
3. Palette-based interior components → 100 per frame, constant area.
4. Tracking: Hungarian on previous positions; tried constant-velocity and physics predictors to cross-check.
   Constant-velocity disagreed after frame 603 (an impossible 38 px jump) → rejected.
5. Rounded centres at frames 211/348/592; read "28" from the last-frame crop → Check passed.
