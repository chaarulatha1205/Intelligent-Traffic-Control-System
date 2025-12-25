import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from torch_geometric.data import Data, DataLoader

class TrafficDataset:
    """Generate training data for GNN"""
    
    def __init__(self):
        self.junctions = 5
        self.features = 6
        
    def generate_data(self, samples=1000):
        """Generate synthetic training data"""
        data_list = []
        
        for _ in range(samples):
            # Node features (random traffic data)
            x = torch.randn(self.junctions, self.features)
            
            # Edge connections (fully connected for demo)
            edge_index = []
            for i in range(self.junctions):
                for j in range(self.junctions):
                    if i != j:
                        edge_index.append([i, j])
            
            edge_index = torch.tensor(edge_index, dtype=torch.long).t()
            
            # Labels (optimal signal durations)
            y = torch.randint(20, 60, (self.junctions, 4)).float()
            
            data = Data(x=x, edge_index=edge_index, y=y)
            data_list.append(data)
        
        return data_list

def train_model():
    """Train GNN model"""
    print("Training GNN model...")
    
    # Generate dataset
    dataset = TrafficDataset().generate_data(500)
    train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Define model
    model = nn.Sequential(
        nn.Linear(6, 64),
        nn.ReLU(),
        nn.Linear(64, 128),
        nn.ReLU(),
        nn.Linear(128, 4)  # 4 phase durations
    )
    
    # Training
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(10):
        total_loss = 0
        for data in train_loader:
            optimizer.zero_grad()
            output = model(data.x)
            loss = criterion(output, data.y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_loader):.4f}")
    
    # Save model
    torch.save(model.state_dict(), 'models/traffic_gnn.pth')
    print("Model saved to models/traffic_gnn.pth")

if __name__ == "__main__":
    train_model()