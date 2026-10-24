from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Step 1: Define the structure of the Bayesian Network
model = DiscreteBayesianNetwork([
    ('Rain', 'Maintenance'),
    ('Rain', 'Train'),
    ('Maintenance', 'Train'),
    ('Train', 'Appointment')
])

# Step 2: Define the CPDs with state names

# Rain: none (0), light (1), heavy (2)
cpd_rain = TabularCPD(
    variable='Rain',
    variable_card=3,
    values=[
        [0.5],
        [0.3],
        [0.2]
    ],
    state_names={'Rain': ['none', 'light', 'heavy']}
)

# Maintenance depends on Rain
# Maintenance: yes (0), no (1)
cpd_maintenance = TabularCPD(
    variable='Maintenance',
    variable_card=2,
    values=[
        [0.2,    0.4,   0.8],
        [0.8,    0.6,   0.2]
    ],
    evidence=['Rain'],
    evidence_card=[3],
    state_names={
        'Maintenance': ['yes', 'no'],
        'Rain': ['none', 'light', 'heavy']
    }
)

# Train depends on Rain and Maintenance
# Train: on_time (0), delayed (1)
cpd_train = TabularCPD(
    variable='Train',
    variable_card=2,
   
    values=[
        # on_time
        [0.9, 0.95, 0.7, 0.8, 0.3, 0.5],
        # delayed
        [0.1, 0.05, 0.3, 0.2, 0.7, 0.5]
    ],
    evidence=['Rain', 'Maintenance'],
    evidence_card=[3, 2],
    state_names={
        'Train': ['on_time', 'delayed'],
        'Rain': ['none', 'light', 'heavy'],
        'Maintenance': ['yes', 'no']
    }
)

# Appointment depends on Train
# Appointment: attend (0), miss (1)
cpd_appointment = TabularCPD(
    variable='Appointment',
    variable_card=2,
    values=[
        # Train: on_time, delayed
        [0.95, 0.6],
        [0.05, 0.4]
    ],
    evidence=['Train'],
    evidence_card=[2],
    state_names={
        'Appointment': ['attend', 'miss'],
        'Train': ['on_time', 'delayed']
    }
)

# Step 3: Add CPDs to the model
model.add_cpds(cpd_rain, cpd_maintenance, cpd_train, cpd_appointment)

# Step 4: Check if the model is valid
assert model.check_model(), "Model structure or CPDs are invalid."

# Step 5: Inference Engine
inference = VariableElimination(model)

# Step 6: Example Inferences

print("\n1. P(Appointment)")
print(inference.query(variables=['Appointment']))

print("\n2. P(Appointment | Rain=light, Maintenance=no)")
print(inference.query(
    variables=['Appointment'],
    evidence={'Rain': 'light', 'Maintenance': 'no'}
))

print("\n3. P(Appointment | Train=delayed)")
print(inference.query(
    variables=['Appointment'],
    evidence={'Train': 'delayed'}
))

print("\n4. P(Rain | Appointment=attend)")
print(inference.query(
    variables=['Rain'],
    evidence={'Appointment': 'attend'}
))
