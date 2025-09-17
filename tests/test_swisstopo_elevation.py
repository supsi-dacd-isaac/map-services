"""
Tests for Swiss Topo elevation services.
"""

import pytest
from unittest.mock import Mock, patch
from map_services.swisstopo_elevation import (
    SwissTopoElevationClient,
    get_elevation,
    get_elevation_batch
)


class TestSwissTopoElevationClient:
    """Test cases for SwissTopoElevationClient class."""
    
    def test_client_initialization(self):
        """Test that client initializes correctly."""
        client = SwissTopoElevationClient()
        assert client.base_url == "https://api3.geo.admin.ch/rest/services/height"
        assert client.session is not None
    
    def test_client_initialization_custom_url(self):
        """Test client initialization with custom URL."""
        custom_url = "https://custom.api.com/height"
        client = SwissTopoElevationClient(base_url=custom_url)
        assert client.base_url == custom_url
    
    @patch('requests.Session.get')
    def test_get_elevation_success(self, mock_get):
        """Test successful elevation retrieval."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {'height': 1200.5}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        client = SwissTopoElevationClient()
        elevation = client.get_elevation(8.5417, 47.3769)  # Zurich coordinates
        
        assert elevation == 1200.5
        mock_get.assert_called_once()
    
    @patch('requests.Session.get')
    def test_get_elevation_failure(self, mock_get):
        """Test elevation retrieval failure."""
        # Mock exception
        mock_get.side_effect = Exception("API Error")
        
        client = SwissTopoElevationClient()
        elevation = client.get_elevation(8.5417, 47.3769)
        
        assert elevation is None
    
    @patch('requests.Session.get')
    def test_get_elevation_no_height_data(self, mock_get):
        """Test elevation retrieval when no height data is available."""
        # Mock response without height
        mock_response = Mock()
        mock_response.json.return_value = {'error': 'No data'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        client = SwissTopoElevationClient()
        elevation = client.get_elevation(8.5417, 47.3769)
        
        assert elevation is None
    
    def test_get_elevation_batch(self):
        """Test batch elevation retrieval."""
        client = SwissTopoElevationClient()
        
        # Mock the get_elevation method
        with patch.object(client, 'get_elevation') as mock_get_elevation:
            mock_get_elevation.side_effect = [1200.5, 1500.0, None]
            
            coordinates = [
                (8.5417, 47.3769),  # Zurich
                (7.4474, 46.9480),  # Bern
                (0.0, 0.0)          # Invalid
            ]
            
            elevations = client.get_elevation_batch(coordinates)
            
            assert elevations == [1200.5, 1500.0, None]
            assert mock_get_elevation.call_count == 3
    
    def test_get_elevation_batch_empty_list(self):
        """Test batch elevation with empty coordinate list."""
        client = SwissTopoElevationClient()
        elevations = client.get_elevation_batch([])
        assert elevations == []


class TestConvenienceFunctions:
    """Test cases for convenience functions."""
    
    @patch('map_services.swisstopo_elevation.SwissTopoElevationClient')
    def test_get_elevation_function(self, mock_client_class):
        """Test the get_elevation convenience function."""
        # Setup mock
        mock_client = Mock()
        mock_client.get_elevation.return_value = 1200.5
        mock_client_class.return_value = mock_client
        
        elevation = get_elevation(8.5417, 47.3769)
        
        assert elevation == 1200.5
        mock_client_class.assert_called_once()
        mock_client.get_elevation.assert_called_once_with(8.5417, 47.3769)
    
    @patch('map_services.swisstopo_elevation.SwissTopoElevationClient')
    def test_get_elevation_batch_function(self, mock_client_class):
        """Test the get_elevation_batch convenience function."""
        # Setup mock
        mock_client = Mock()
        mock_client.get_elevation_batch.return_value = [1200.5, 1500.0]
        mock_client_class.return_value = mock_client
        
        coordinates = [(8.5417, 47.3769), (7.4474, 46.9480)]
        elevations = get_elevation_batch(coordinates)
        
        assert elevations == [1200.5, 1500.0]
        mock_client_class.assert_called_once()
        mock_client.get_elevation_batch.assert_called_once_with(coordinates)


class TestIntegration:
    """Integration tests that verify the package works as expected."""
    
    def test_package_import(self):
        """Test that the package can be imported successfully."""
        import map_services
        assert hasattr(map_services, 'swisstopo_elevation')
    
    def test_module_attributes(self):
        """Test that the module has expected attributes."""
        from map_services import swisstopo_elevation
        
        assert hasattr(swisstopo_elevation, 'SwissTopoElevationClient')
        assert hasattr(swisstopo_elevation, 'get_elevation')
        assert hasattr(swisstopo_elevation, 'get_elevation_batch')
    
    def test_client_creation(self):
        """Test that we can create a client instance."""
        client = SwissTopoElevationClient()
        assert isinstance(client, SwissTopoElevationClient)
        assert hasattr(client, 'get_elevation')
        assert hasattr(client, 'get_elevation_batch')


if __name__ == '__main__':
    pytest.main([__file__])