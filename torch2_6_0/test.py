import torch
import torch.nn as nn
import torch.optim as optim
import platform

# CPU Info
print(f"PyTorch version: {torch.__version__}")
print(f"Operating System: {platform.system()} {platform.release()}")
print(f"Processor: {platform.processor()}")
print(f"CUDA available: {torch.cuda.is_available()}")

# GPU Info (if available)
if torch.cuda.is_available():
    print(f"GPU Device Count: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

print(f"Using device: {device}")

# Define a simple neural network
class SimpleNN(nn.Module):
    def __init__(self, input_size=10, hidden_size=16, output_size=1):
        super(SimpleNN, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x):
        return self.model(x)

# Instantiate the model and move to device
model = SimpleNN().to(device)

# Dummy input and target
x = torch.randn(64, 10).to(device)  # batch size 64, input size 10
y = torch.randn(64, 1).to(device)

# Define loss and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train for a few steps
print("Training...")
for step in range(5):
    model.train()
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    print(f"Step {step+1}, Loss: {loss.item():.4f}")

print("Test completed.")