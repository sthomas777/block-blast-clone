# BLOCK BLAST GAME MADE IN PYTHON

# Overview

This is a fun little block blast clone I decided to create over the summer after the recovery of my ear surgery. This project was designed using all the principles I learned from my internship at Rapid7. In addition, I wanted to deepen my technical knowledge by learning new technologies.
More info: WHY_THIS_PROJECT.md

## Prerequisites

1. Make sure `uv`, `npm` and `docker-desktop` is installed
2. Once you clone the repo you will need to make a `secrets/` folder inside the root and have the following `.txt` files
   - `db_name.txt`
   - `db_password.txt`
   - `db_user.txt`
   - `secret_key.txt` <- Key for hashing password

### How to Play

Install deps by running:

```
make install
```

Go to the root directory of the project and run:

```bash
make play
```

Once that runs, press the URL:

```
http://localhost:3000
```

Register/Sign in and play the block blast clone.

### Demo


https://github.com/user-attachments/assets/914815b4-579d-4ed0-903a-275b9cae7091


### Running Tests

Use the following commands to run tests:

- `make test`: Runs frontend and backend tests (No backend integration tests)
- `make test-backend`: Runs backend unit tests ONLY
- `make test-frontend`: Runs frontend unit tests ONLY
- `make test-integration`: Runs backend integration tests ONLY
- `make test-coverage`: Test coverage of both backend and frontend
