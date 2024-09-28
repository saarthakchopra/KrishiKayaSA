# KrishiKaya

## Installation

### 1. Clone the repository:
```
git clone https://github.com/KhushiAgarwal22/KrishiKaya.git cd KrishiKaya/Backend/inventoryMarketPlace
```
### 2. Install the required packages for the Django backend:
```
pip install django pillow numpy pandas django-pandas plotly
```
### 3. Navigate to the Frontend directory and install the required packages for the React frontend:
```
cd ../Frontend
npm install
```
## Running the Project
To run both the Django server and React frontend simultaneously, you can use the provided run.sh script located in the root of the repository. Before running the script, make sure to grant executable permissions:
```
chmod +x run.sh
```
Then execute the following command from the root directory:
```
./run.sh
```
Alternatively, if you prefer to run the servers separately, you can start the Django server with:
```
cd Backend/inventoryMarketPlace
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
And in another terminal, start the React frontend with:
```
cd Frontend
npm start
```
